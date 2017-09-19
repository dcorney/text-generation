import logging
import time
import concurrent.futures
import database.text_importer as textim

logger = logging.getLogger(__name__)

# Download file from Gutenburg and run through tokenizer / NER, storing results in S3
# Uses concurrent execution.
# TODO: rename module & functions to something sensible!

def process_one_gut_file(file_id):
    ti = textim.TextImporter()
    ti.doc_from_gut(file_id)
    ti.doc_to_cache()
    ti.doc_to_s3()
    sents = ti.doc_to_sentences()
    tokens_ner = ti.sents_to_tokens(sents)
    ti.tokens_to_s3(sents, tokens_ner, file_id)
    return tokens_ner

def serial(file_ids):
    for id in file_ids:
        ts = process_one_gut_file(id)
        print("{} has {} tokens".format(id, len(ts)))



def parallel(file_ids):    
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_one_gut_file, file_id): file_id for file_id in file_ids}
        for future in concurrent.futures.as_completed(futures):
            file_id = futures[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (file_id, exc))
                raise exc
            else:
                print('%s file is %d long' % (file_id, len(data)))


def dev():
    file_ids = [125,126,128,130,132]

    print("Serial")
    start_time = time.perf_counter()
    serial(file_ids)
    elapsed_time = time.perf_counter() - start_time
    s_elapsed_time=elapsed_time
    print(s_elapsed_time)

    print('\nParallel')
    start_time = time.perf_counter()
    parallel(file_ids)

    p_elapsed_time = time.perf_counter() - start_time
    print(p_elapsed_time)

    print("\nSerial {:0.3f}   Parallel {:0.3f}   Ratio {:0.3f}".format(s_elapsed_time, p_elapsed_time, p_elapsed_time/s_elapsed_time))
