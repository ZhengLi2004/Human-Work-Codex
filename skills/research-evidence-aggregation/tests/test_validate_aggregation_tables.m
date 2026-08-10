function tests = test_validate_aggregation_tables
    %TEST_VALIDATE_AGGREGATION_TABLES Build the local MATLAB test suite.
    tests = functiontests(localfunctions);
end

function setupOnce(testCase)
    %SETUPONCE Add the aggregation-validation assets to the MATLAB path.
    assetDirectory = fullfile(fileparts(fileparts(mfilename("fullpath"))), "assets");
    addpath(assetDirectory);
    testCase.TestData.assetDirectory = assetDirectory;
end

function teardownOnce(testCase)
    %TEARDOWNONCE Remove the aggregation-validation assets from the MATLAB path.
    rmpath(testCase.TestData.assetDirectory);
end

function testValidTablesPass(testCase)
    %TESTVALIDTABLESPASS Accept a complete internally consistent fixture.
    [planned, runs, aggregateFull, spec] = validFixture();
    validation = validate_aggregation_tables(planned, runs, aggregateFull, spec);
    verifyTrue(testCase, validation.passed);
end

function testDuplicateStableRunKeyFails(testCase)
    %TESTDUPLICATESTABLERUNKEYFAILS Detect a duplicate stable run identifier.
    [planned, runs, aggregateFull, spec] = validFixture();
    runs.run_id(4) = runs.run_id(3);
    validation = validate_aggregation_tables(planned, runs, aggregateFull, spec);
    verifyFailedCheck(testCase, validation, "stable_run_key_uniqueness");
end

function testJoinExpansionFails(testCase)
    %TESTJOINEXPANSIONFAILS Detect a declared join-cardinality expansion.
    [planned, runs, aggregateFull, spec] = validFixture();
    spec.join_audits.joined_rows = 7;
    validation = validate_aggregation_tables(planned, runs, aggregateFull, spec);
    verifyFailedCheck(testCase, validation, "join_cardinality_condition_metadata");
end

function testMissingPlannedConditionFails(testCase)
    %TESTMISSINGPLANNEDCONDITIONFAILS Detect incomplete planned-condition coverage.
    [planned, runs, aggregateFull, spec] = validFixture();
    aggregateFull(2, :) = [];
    validation = validate_aggregation_tables(planned, runs, aggregateFull, spec);
    verifyFailedCheck(testCase, validation, "planned_condition_coverage");
end

function testStatusCountMismatchFails(testCase)
    %TESTSTATUSCOUNTMISMATCHFAILS Detect an aggregate status-count mismatch.
    [planned, runs, aggregateFull, spec] = validFixture();
    aggregateFull.n_failed(2) = 0;
    validation = validate_aggregation_tables(planned, runs, aggregateFull, spec);
    verifyFailedCheck(testCase, validation, "status_count_failed");
end

function testWrongDenominatorResultFails(testCase)
    %TESTWRONGDENOMINATORRESULTFAILS Detect an incorrect reported rate.
    [planned, runs, aggregateFull, spec] = validFixture();
    aggregateFull.trials(2) = 5;
    validation = validate_aggregation_tables(planned, runs, aggregateFull, spec);
    verifyFailedCheck(testCase, validation, "rate_identity_success_rate");
end

function [planned, runs, aggregateFull, spec] = validFixture()
    %VALIDFIXTURE Build a complete valid aggregation fixture.
    %   [PLANNED, RUNS, AGGREGATEFULL, SPEC] = VALIDFIXTURE() returns matching
    %   planned, run-level, aggregate, and validation-specification data.
    condition = ["A"; "A"; "B"; "B"];
    repeat_id = [1; 2; 1; 2];
    planned = table(condition, repeat_id);
    run_id = ["A-1"; "A-2"; "B-1"; "B-2"];
    status = ["complete"; "complete"; "complete"; "failed"];
    runs = table(condition, repeat_id, run_id, status);
    condition = ["A"; "B"];
    n_planned = [2; 2];
    n_valid = [2; 1];
    n_complete = [2; 1];
    n_failed = [0; 1];
    successes = [1; 2];
    trials = [2; 4];
    success_rate = [0.5; 0.5];

    aggregateFull = table(condition, n_planned, n_valid, n_complete, n_failed, ...
        successes, trials, success_rate);

    spec = struct;
    spec.condition_keys = "condition";
    spec.run_keys = "run_id";
    spec.status_column = "status";
    spec.valid_statuses = "complete";
    spec.status_count_columns = struct("complete", "n_complete", "failed", "n_failed");

    spec.join_audits = struct("name", "condition_metadata", "left_rows", 4, ...
        "right_rows", 2, "joined_rows", 4, "expected_max_rows", 4);

    spec.rate_checks = struct("id", "success_rate", "numerator_column", "successes", ...
        "denominator_column", "trials", "value_column", "success_rate", ...
        "tolerance", 1e-12);
end

function verifyFailedCheck(testCase, validation, expectedId)
    %VERIFYFAILEDCHECK Verify one expected blocking validation check.
    %   VERIFYFAILEDCHECK(TESTCASE, VALIDATION, EXPECTEDID) requires a failed
    %   overall result and the requested failed-check identifier.
    failedIds = string({validation.checks(strcmp({validation.checks.status}, "fail")).id});
    verifyFalse(testCase, validation.passed);

    verifyTrue(testCase, any(failedIds == expectedId), ...
        "Expected failed check was not present: " + expectedId);
end
