import logging
import time
import concurrent.futures
import database.text_importer as textim

logger = logging.getLogger(__name__)


# def load_text(file_id):
#     with open("/Users/dcorney/temp/{}.txt".format(file_id)) as file_in:
#         text = file_in.read()
#         text = text[0:50000]
#     TI = textim.TextImporter()
#     TI._doc = {"title": "A title", "text": text, "id": file_id}
#     # TI.doc_from_gut(id, max_len=500)
#     TI.doc_to_cache()
#     # TI.doc_to_s3()
#     return TI._doc


# def tokenize(file_id):
#     doc = load_text(file_id)
#     TI = textim.TextImporter()
#     TI._doc = {"title": doc['title'], "text": doc['text'], "id": file_id}
#     sents = TI.doc_to_sentences()
#     print("Text: {} Sents: {}".format(len(doc['text']), len(sents)))
#     tokens_ner = TI.sents_to_tokens(sents)
#     print(len(tokens_ner))
#     TI.tokens_to_s3(sents, tokens_ner, file_id)
#     return tokens_ner



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
