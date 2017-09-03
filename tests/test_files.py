from context import files
import random

# Include a randon number so that multiple runs of the
# test don't read the version of the file previously written
test_obj={"title":"This is the title",
          "text":"this is the content",
          "id":random.randint(0,999999)}

def test_s3_write():
    cloud = files.files(files.Storage_type.s3)
    cloud.write_text_s3(test_obj, "test_obj.json")
    froms3_obj = cloud.read_text_s3("test_obj.json")
    print(froms3_obj)
    print(test_obj)
    assert froms3_obj == test_obj

