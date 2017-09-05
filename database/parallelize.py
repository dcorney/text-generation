import logging
import time
import concurrent.futures
import database.text_importer as textim

logger = logging.getLogger("textgen." + __name__)


def process_one_gut_file(file_id):
    ti = textim.TextImporter()
    ti.doc_from_gut(file_id)
    ti.doc_to_cache()
    ti.doc_to_s3()
    sents = ti.doc_to_sentences()
    logger.info("Found {} sentences".format(len(sents)))
    tokens_ner = ti.sents_to_tokens(sents)
    ti.tokens_to_s3(sents, tokens_ner, file_id)
    logger.info("Wrote to S3")
    return tokens_ner


def serial(file_ids):
    for id in file_ids:
        ts = process_one_gut_file(id)
        print("{} has {} tokens".format(id, len(ts)))



def parallel(file_ids):
    logger.info("Submitting job for {} files ".format(len(file_ids)))
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_one_gut_file, file_id): file_id for file_id in file_ids}
        for future in concurrent.futures.as_completed(futures):
            file_id = futures[future]
            logger.info("Future completed file {}".format(file_id))
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (file_id, exc))
                raise exc
            else:
                logger.info('%s file is %d long' % (file_id, len(data)))


def dev():
    exclusions = [101, 104, 106, 114, 115, 118, 124, 127, 129, 131, 180,
                 200, 226, 227, 229, 230, 228, 231, 232, 247, 248, 258, 266, 277, 278]

    # file_ids = [125,126,128,130,132]
    s = set(range(102,600))
    file_ids = [x for x in s if x not in exclusions]

    # print("Serial")
    # start_time = time.perf_counter()
    # serial(file_ids)
    # elapsed_time = time.perf_counter() - start_time
    # s_elapsed_time=elapsed_time
    # print(s_elapsed_time)
    logger.info("Starting parallel process")
    print('\nParallel')
    start_time = time.perf_counter()
    parallel(file_ids)

    p_elapsed_time = time.perf_counter() - start_time
    logger.info("Total elapsed time: {} for {} files ".format(p_elapsed_time,len(file_ids)))

    # print("\nSerial {:0.3f}   Parallel {:0.3f}   Ratio {:0.3f}".format(s_elapsed_time, p_elapsed_time, p_elapsed_time/s_elapsed_time))
