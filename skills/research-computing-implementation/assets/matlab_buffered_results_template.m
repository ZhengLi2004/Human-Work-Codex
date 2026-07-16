function run_buffered_results(taskTable, outputDir, tasksPerChunk)
%RUN_BUFFERED_RESULTS Template for chunked, worker-isolated result writes.
%
% Adapt COMPUTE_ONE_TASK and the result schema to the TODO. Each PARFOR
% iteration computes a meaningful chunk and publishes one immutable Parquet
% file. Do not call WRITETABLE once per result row.

arguments
    taskTable table
    outputDir (1,1) string
    tasksPerChunk (1,1) double {mustBeInteger, mustBePositive} = 1000
end

if ~isfolder(outputDir)
    mkdir(outputDir);
end

nTasks = height(taskTable);
nChunks = ceil(nTasks / tasksPerChunk);

parfor chunkId = 1:nChunks
    firstRow = (chunkId - 1) * tasksPerChunk + 1;
    lastRow = min(chunkId * tasksPerChunk, nTasks);
    rows = firstRow:lastRow;

    finalPath = fullfile(outputDir, sprintf("part-%06d.parquet", chunkId));
    expectedTaskIds = string(taskTable.task_id(rows));
    if isfile(finalPath)
        existing = parquetread(finalPath, ...
            "SelectedVariableNames", "task_id");
        assert(isequal(string(existing.task_id), expectedTaskIds), ...
            "Existing immutable chunk does not match expected tasks: %s", finalPath);
        continue
    end

    % Preallocate a bounded structure array for this chunk.
    template = struct( ...
        "task_id", "", ...
        "condition", "", ...
        "repeat", NaN, ...
        "metric", NaN, ...
        "state", "pending", ...
        "error", "");
    records = repmat(template, numel(rows), 1);

    for localIdx = 1:numel(rows)
        task = taskTable(rows(localIdx), :);
        records(localIdx).task_id = string(task.task_id);
        records(localIdx).condition = string(task.condition);
        records(localIdx).repeat = double(task.repeat);
        try
            records(localIdx).metric = compute_one_task(task);
            records(localIdx).state = "complete";
        catch exception
            records(localIdx).state = "failed";
            records(localIdx).error = string(getReport(exception, "extended", ...
                "hyperlinks", "off"));
        end
    end

    chunkTable = struct2table(records);
    tempPath = finalPath + ".tmp";
    if isfile(tempPath)
        delete(tempPath);
    end

    parquetwrite(tempPath, chunkTable);
    checkTable = parquetread(tempPath, "SelectedVariableNames", "task_id");
    assert(height(checkTable) == height(chunkTable), ...
        "Chunk row-count validation failed: %s", tempPath);
    movefile(tempPath, finalPath);
end
end

function metric = compute_one_task(task)
% Replace this placeholder with the TODO-defined, vectorized computation.
metric = double(task.value);
end
