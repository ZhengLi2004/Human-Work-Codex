function validation = validate_aggregation_tables(planned, runs, aggregateFull, spec)
    %VALIDATE_AGGREGATION_TABLES Check common aggregation integrity contracts.
    %   VALIDATION = VALIDATE_AGGREGATION_TABLES(PLANNED, RUNS, AGGREGATEFULL,
    %   SPEC) checks stable keys, complete planned coverage, status counts,
    %   declared join audits, and configured numerator/denominator identities.
    %
    %   Required SPEC fields:
    %     condition_keys  cell array or string array of aggregate-grain keys
    %     run_keys        cell array or string array of independent-run keys
    %     status_column   run status variable name
    %
    %   Optional SPEC fields:
    %     n_planned_column     default "n_planned"
    %     n_valid_column       default "n_valid"
    %     valid_statuses       default "complete"
    %     status_count_columns scalar struct mapping status to aggregate column
    %     join_audits          struct array with name, left_rows, right_rows,
    %                          joined_rows, and expected_max_rows
    %     rate_checks          struct array with id, numerator_column,
    %                          denominator_column, value_column, and tolerance
    %
    %   This function validates generic table contracts only. The caller must
    %   still record source authority, fingerprints, TODO-specific ranges,
    %   time coverage, scientific formulas, and evidence paths in
    %   aggregation-validation.json.
    %
    % Inputs:
    %   planned       Planned-condition table at the declared run grain.
    %   runs          Observed run table containing stable keys and status.
    %   aggregateFull Aggregate table containing every planned condition.
    %   spec          Validation field names and optional audit definitions.
    %
    % Output:
    %   validation    Struct containing checks, pass state, and blocking IDs.

    arguments
        planned table
        runs table
        aggregateFull table
        spec struct
    end

    conditionKeys = reshape(string(spec.condition_keys), 1, []);
    runKeys = reshape(string(spec.run_keys), 1, []);
    statusColumn = string(spec.status_column);
    nPlannedColumn = optionalString(spec, "n_planned_column", "n_planned");
    nValidColumn = optionalString(spec, "n_valid_column", "n_valid");
    validStatuses = optionalStrings(spec, "valid_statuses", "complete");
    requireVariables(planned, conditionKeys, "planned");
    requireVariables(runs, [conditionKeys, runKeys, statusColumn], "runs");
    requireVariables(aggregateFull, conditionKeys, "aggregateFull");
    checks = emptyChecks();
    % Validate stable run identity before any count reconciliation.
    runIdentity = stableRowKeys(runs, runKeys);
    duplicateRunCount = numel(runIdentity) - numel(unique(runIdentity));

    checks(end + 1) = makeCheck("stable_run_key_uniqueness", ...
        passFail(duplicateRunCount == 0), ...
        struct("duplicate_row_count", duplicateRunCount), ...
        struct("duplicate_row_count", 0), ...
        "blocks_use", "runs");

    % Validate aggregate identity and complete planned-condition coverage.
    plannedCondition = stableRowKeys(planned, conditionKeys);
    aggregateCondition = stableRowKeys(aggregateFull, conditionKeys);
    duplicateAggregateCount = numel(aggregateCondition) - numel(unique(aggregateCondition));

    checks(end + 1) = makeCheck("aggregate_condition_key_uniqueness", ...
        passFail(duplicateAggregateCount == 0), ...
        struct("duplicate_row_count", duplicateAggregateCount), ...
        struct("duplicate_row_count", 0), ...
        "blocks_use", "aggregate_full");

    plannedUnique = unique(plannedCondition, "stable");
    aggregateUnique = unique(aggregateCondition, "stable");
    missingConditions = setdiff(plannedUnique, aggregateUnique, "stable");
    extraConditions = setdiff(aggregateUnique, plannedUnique, "stable");

    checks(end + 1) = makeCheck("planned_condition_coverage", ...
        passFail(isempty(missingConditions) && isempty(extraConditions)), ...
        struct("missing_keys", missingConditions, "extra_keys", extraConditions), ...
        struct("missing_keys", strings(0, 1), "extra_keys", strings(0, 1)), ...
        "blocks_use", "planned and aggregate_full");

    % Reconcile optional planned and valid counts against source rows.

    if ismember(nPlannedColumn, string(aggregateFull.Properties.VariableNames))
        expectedPlanned = countsForKeys(plannedCondition, aggregateCondition);
        actualPlanned = double(aggregateFull.(nPlannedColumn));

        checks(end + 1) = numericVectorCheck("planned_count_reconciliation", ...
            actualPlanned, expectedPlanned, 0, "blocks_use", "planned and aggregate_full");
    end

    runCondition = stableRowKeys(runs, conditionKeys);
    runStatuses = string(runs.(statusColumn));

    if ismember(nValidColumn, string(aggregateFull.Properties.VariableNames))
        isValid = ismember(runStatuses, validStatuses);
        expectedValid = countsForKeys(runCondition(isValid), aggregateCondition);
        actualValid = double(aggregateFull.(nValidColumn));

        checks(end + 1) = numericVectorCheck("valid_count_reconciliation", ...
            actualValid, expectedValid, 0, "blocks_use", "runs and aggregate_full");
    end

    if isfield(spec, "status_count_columns")
        mappings = spec.status_count_columns;
        statuses = string(fieldnames(mappings));

        % Reconcile every declared status count independently.

        for index = 1:numel(statuses)
            status = statuses(index);
            aggregateColumn = string(mappings.(status));
            requireVariables(aggregateFull, aggregateColumn, "aggregateFull");
            expectedStatus = countsForKeys(runCondition(runStatuses == status), aggregateCondition);
            actualStatus = double(aggregateFull.(aggregateColumn));

            checks(end + 1) = numericVectorCheck("status_count_" + status, ...
                actualStatus, expectedStatus, 0, "blocks_use", "runs and aggregate_full");
        end

    end

    % Validate declared join cardinality limits.

    if isfield(spec, "join_audits")
        joinAudits = spec.join_audits;

        for index = 1:numel(joinAudits)
            audit = joinAudits(index);
            passed = double(audit.joined_rows) <= double(audit.expected_max_rows);

            checks(end + 1) = makeCheck("join_cardinality_" + string(audit.name), ...
                passFail(passed), ...
                struct("left_rows", double(audit.left_rows), ...
                "right_rows", double(audit.right_rows), ...
                "joined_rows", double(audit.joined_rows)), ...
                struct("maximum_joined_rows", double(audit.expected_max_rows)), ...
                "blocks_use", "join audit " + string(audit.name));
        end

    end

    % Recompute declared rates from their numerator and denominator columns.

    if isfield(spec, "rate_checks")
        rateChecks = spec.rate_checks;

        for index = 1:numel(rateChecks)
            rateCheck = rateChecks(index);
            numeratorColumn = string(rateCheck.numerator_column);
            denominatorColumn = string(rateCheck.denominator_column);
            valueColumn = string(rateCheck.value_column);
            requireVariables(aggregateFull, [numeratorColumn, denominatorColumn, valueColumn], "aggregateFull");
            numerator = double(aggregateFull.(numeratorColumn));
            denominator = double(aggregateFull.(denominatorColumn));
            reported = double(aggregateFull.(valueColumn));
            expected = numerator ./ denominator;
            zeroDenominator = denominator == 0;
            tolerance = double(rateCheck.tolerance);
            mismatch = ~(abs(reported - expected) <= tolerance | (isnan(reported) & isnan(expected)));
            passed = ~any(zeroDenominator) && ~any(mismatch);

            checks(end + 1) = makeCheck("rate_identity_" + string(rateCheck.id), ...
                passFail(passed), ...
                struct("zero_denominator_rows", find(zeroDenominator), ...
                "mismatch_rows", find(mismatch), ...
                "maximum_absolute_error", max(abs(reported - expected), [], "omitnan")), ...
                struct("zero_denominator_rows", zeros(0, 1), ...
                "mismatch_rows", zeros(0, 1), ...
                "tolerance", tolerance), ...
                "blocks_use", "aggregate_full");
        end

    end

    % Assemble the deterministic machine-readable validation result.

    failed = string({checks(strcmp({checks.status}, "fail")).id});

    validation = struct( ...
        "schema_version", 1, ...
        "passed", isempty(failed), ...
        "analysis_grain", conditionKeys, ...
        "stable_run_keys", runKeys, ...
        "checks", checks, ...
        "blocking_findings", failed);
end

function value = optionalString(spec, field, defaultValue)
    %OPTIONALSTRING Read an optional scalar string field.
    %   VALUE = OPTIONALSTRING(SPEC, FIELD, DEFAULTVALUE) returns SPEC.(FIELD)
    %   as a string when present and otherwise returns DEFAULTVALUE as a string.

    if isfield(spec, field)
        value = string(spec.(field));
    else
        value = string(defaultValue);
    end

end

function value = optionalStrings(spec, field, defaultValue)
    %OPTIONALSTRINGS Read an optional string-vector field.
    %   VALUE = OPTIONALSTRINGS(SPEC, FIELD, DEFAULTVALUE) returns the selected
    %   value as a row string array.

    if isfield(spec, field)
        value = reshape(string(spec.(field)), 1, []);
    else
        value = reshape(string(defaultValue), 1, []);
    end

end

function requireVariables(inputTable, variables, tableName)
    %REQUIREVARIABLES Require named variables in a table.
    %   REQUIREVARIABLES(INPUTTABLE, VARIABLES, TABLENAME) raises a namespaced
    %   error that identifies every missing variable.
    missing = setdiff(string(variables), string(inputTable.Properties.VariableNames), "stable");

    if ~isempty(missing)
        error("ResearchTaskSystem:MissingVariable", ...
            "%s is missing required variables: %s", tableName, strjoin(missing, ", "));
    end

end

function keys = stableRowKeys(inputTable, variables)
    %STABLEROWKEYS Encode table rows as deterministic composite string keys.
    %   KEYS = STABLEROWKEYS(INPUTTABLE, VARIABLES) preserves missing values,
    %   datetime precision, variable order, and literal separator characters.
    values = table2cell(inputTable(:, cellstr(variables)));
    parts = strings(height(inputTable), numel(variables));

    for column = 1:numel(variables)

        for row = 1:height(inputTable)
            value = values{row, column};

            if ismissingScalar(value)
                text = "<missing>";
            elseif isdatetime(value)
                text = string(value, "yyyy-MM-dd'T'HH:mm:ss.SSSXXX");
            else
                text = string(value);
            end

            parts(row, column) = replace(text, "|", "||");
        end

    end

    keys = join(parts, "|", 2);
end

function result = ismissingScalar(value)
    %ISMISSINGSCALAR Test one heterogeneous table value for missingness.
    %   RESULT = ISMISSINGSCALAR(VALUE) returns false when the value class does
    %   not implement a compatible ISMISSING operation.

    try
        missingValue = ismissing(value);
        result = isscalar(missingValue) && missingValue;
    catch
        result = false;
    end

end

function counts = countsForKeys(sourceKeys, targetKeys)
    %COUNTSFORKEYS Count source-key occurrences in target-key order.
    %   COUNTS = COUNTSFORKEYS(SOURCEKEYS, TARGETKEYS) returns zero for every
    %   target key absent from SOURCEKEYS.
    if isempty(sourceKeys)
        counts = zeros(numel(targetKeys), 1);
        return
    end

    [uniqueKeys, ~, groups] = unique(sourceKeys, "stable");
    sourceCounts = accumarray(groups, 1, [numel(uniqueKeys), 1]);
    [found, locations] = ismember(targetKeys, uniqueKeys);
    counts = zeros(numel(targetKeys), 1);
    counts(found) = sourceCounts(locations(found));
end

function check = numericVectorCheck(id, actual, expected, tolerance, impact, evidence)
    %NUMERICVECTORCHECK Compare numeric vectors with NaN-aware tolerance.
    %   CHECK = NUMERICVECTORCHECK(ID, ACTUAL, EXPECTED, TOLERANCE, IMPACT,
    %   EVIDENCE) returns a normalized validation-check struct.
    mismatch = find(~(abs(actual - expected) <= tolerance | (isnan(actual) & isnan(expected))));

    check = makeCheck(id, passFail(isempty(mismatch)), ...
        struct("mismatch_rows", mismatch, "actual", actual(mismatch)), ...
        struct("mismatch_rows", zeros(0, 1), "expected", expected(mismatch), "tolerance", tolerance), ...
        impact, evidence);
end

function checks = emptyChecks()
    %EMPTYCHECKS Create an empty validation-check struct array.
    checks = struct("id", {}, "status", {}, "observed", {}, "expected", {}, "impact", {}, "evidence", {});
end

function check = makeCheck(id, status, observed, expected, impact, evidence)
    %MAKECHECK Build one normalized validation-check struct.
    %   CHECK = MAKECHECK(ID, STATUS, OBSERVED, EXPECTED, IMPACT, EVIDENCE)
    %   converts identifier-like values to character vectors for JSON output.

    check = struct("id", char(id), "status", char(status), "observed", observed, ...
        "expected", expected, "impact", char(impact), "evidence", char(evidence));
end

function status = passFail(passed)
    %PASSFAIL Convert a logical result to a pass-or-fail status string.

    if passed
        status = "pass";
    else
        status = "fail";
    end

end
