from defects4all.createFastTextTrainSet import create_fasttext_sequence_representation

def test_create_sequence():
    in_dir = "./tests/data/issue_test2"
    vector_representation = create_fasttext_sequence_representation(in_dir, "TestCase")
    with open(vector_representation) as f:
        lines = f.readlines()
    assert(len(lines) == 2)
    assert(lines[1].split()[0] == "__label__AfeDriverTest_pullOutOfReset_success")
    assert(lines[0].split()[0] == "__label__AfeIntestinesTest_afeSetup")

def test_create_sequence_test_suite_level():
    in_dir = "./tests/data/issue_test2"
    vector_representation = create_fasttext_sequence_representation(in_dir, "TestSuite")
    with open(vector_representation) as f:
        lines = f.readlines()
    assert(len(lines) == 2)
    assert(lines[1].split()[0] == "__label__AfeDriverTest")
    assert(lines[0].split()[0] == "__label__AfeIntestinesTest")
