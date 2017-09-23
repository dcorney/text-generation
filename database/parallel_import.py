import time
import concurrent.futures
import core.markovchain as mc
import database.text_importer as text_importer
import logging

logger = logging.getLogger(__name__)


mcW_store = None
ti = None  # TextImporter, to be initialised later


# Update markov-chain from S3 list of tokenized sentences
def s3_to_mc(fileid):
    global mcW_store
    global ti
    sents = ti.tokens_from_s3(fileid)
    if sents:
        logger.info("Adding {} sentences from {} to db".format(len(sents), fileid))
        for s_tokens in sents:
            sent = " ".join(s_tokens)
            mcW_store.add_sentence(sent, 1)
        return 0
    else:
        logger.info("file {} not found".format(fileid))


def parallel_import(fileids):
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(s3_to_mc, fileid): fileid for fileid in fileids}
        for future in concurrent.futures.as_completed(futures):
            file_id = futures[future]
            logger.info("Finished importing {}".format(file_id))
    logger.info("Finished importing all {} files".format(len(fileids)))


def dev():
    print("hello!")
    fileids = range(112, 200)  # [102, 103, 105, 107,108, 109, 110, 111]
    global mcW_store
    mcW_store = mc.MarkovChain()
    global ti
    ti = text_importer.TextImporter()

    # print(store.random_entry())
    # print("Serial test...")
    # start_time = time.perf_counter()
    # s3_to_mc(fileids[0])
    # elapsed_time = time.perf_counter() - start_time
    # s_elapsed_time=elapsed_time
    # print(s_elapsed_time)
    # print("...serial done!")

    start_time = time.perf_counter()
    mass_import(fileids)
    elapsed_time = time.perf_counter() - start_time
    p_elapsed_time = elapsed_time
    print(p_elapsed_time)
    print("...parallel done! {} files".format(len(fileids)))

    # f = files.files(files.Storage_type.s3)
    # f.redis_to_s3()
