function run_buffered_results(taskTable, outputDir, tasksPerChunk)
    %RUN_BUFFERED_RESULTS Template for chunked, worker-isolated result writes.
    %
    % Adapt COMPUTE_ONE_TASK and the result schema to the TODO. Each PARFOR
    % iteration computes a meaningful chunk and publishes one immutable Parquet
    % file. Do not call WRITETABLE once per result row.
    %
    % Inputs:
    %   taskTable     Table containing task_id, condition, repeat, and value.
    %   outputDir     Destination directory for immutable Parquet chunks.
    %   tasksPerChunk Positive integer number of tasks assigned to each chunk.

    arguments
        taskTable table
        outputDir (1, 1) string
        tasksPerChunk (1, 1) double {mustBeInteger, mustBePositive} = 1000
    end

    % Create the destination before scheduling independent chunks.

    if ~isfolder(outputDir)
        mkdir(outputDir);
    end

    nTasks = height(taskTable);
    nChunks = ceil(nTasks / tasksPerChunk);

    % Compute and publish each chunk independently so workers never share a file.

    parfor chunkId = 1:nChunks
        firstRow = (chunkId - 1) * tasksPerChunk + 1;
        lastRow = min(chunkId * tasksPerChunk, nTasks);
        rows = firstRow:lastRow;
        finalPath = fullfile(outputDir, sprintf("part-%06d.parquet", chunkId));
        expectedTaskIds = string(taskTable.task_id(rows));

        % Resume only after the existing immutable chunk matches the task slice.

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

            % Preserve either the metric or complete failure evidence for each task.

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

        % Validate the temporary chunk before the atomic publication step.
        parquetwrite(tempPath, chunkTable);
        checkTable = parquetread(tempPath, "SelectedVariableNames", "task_id");

        assert(height(checkTable) == height(chunkTable), ...
            "Chunk row-count validation failed: %s", tempPath);

        movefile(tempPath, finalPath);
    end

end

function metric = compute_one_task(task)
    %COMPUTE_ONE_TASK Evaluate the placeholder metric for one task row.
    %   METRIC = COMPUTE_ONE_TASK(TASK) converts TASK.value to double. Replace
    %   this body with the TODO-defined computation while preserving the stable
    %   function interface and caller-side failure capture.
    metric = double(task.value);
end
