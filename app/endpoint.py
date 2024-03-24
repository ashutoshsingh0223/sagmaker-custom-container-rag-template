from datetime import datetime
import os
import traceback
import time
import requests

from fastapi import FastAPI, Request
import uvicorn

import processor
import constants



app = FastAPI()


@app.get("/ping")
async def ping():
    return {}


@app.post("/invocations")
async def inference(request: Request):
    print(f"{datetime.now():%H:%M:%S} sleep start.")
    print(os.listdir("/opt/ml/model"))
    manifest = await request.json()

    job_type = manifest['job_type']
    job_name = manifest['job_name']
    file_ids = manifest['file_ids']
    callback_url = manifest['callback_url']

    elastic_host = manifest["elastic_host"]

    if job_type == 'embed':
        query = manifest['query']
        t = transformer.Transformer(
            model_cache_dir=constants.MODEL_CACHE_DIR_HF,
            client=client,
            project=project,
            elastic_host=elastic_host,
            environment=environment
        )

        docs = t.search(query)
        return {"docs": docs}
    else:

        st = time.time()
        import reader
        try:
            documents = manifest['documents']
            r = reader.DocReader(docs=documents)
            t = processor.Processor(
                model_cache_dir="/opt/ml/model",
                client=client,
                project=project,
                elastic_host=elastic_host,
                environment=environment
            )
            lanchain_docs = r.get_documents()
            t.embed_documents(documents=lanchain_docs)

            success = True
            error = ''
        except Exception as e:
            success = False
            error = traceback.format_exc()

        et = time.time()

        callback = {
                        "success": success,
                        "file_ids": file_ids,
                        "job_name": job_name,
                        "time": et - st,
                        "error": error
                    }
        headers = {"Content-Type": "application/json"}
        requests.post(callback_url, json=callback, headers=headers)
   

        callback = {
                        "success": success,
                        "file_ids": file_ids,
                        "job_name": job_name,
                        "time": et - st,
                        "error": error
                    }
        headers = {"Content-Type": "application/json"}
        requests.post(callback_url, json=callback, headers=headers)


    return {"message": "finish"}


@app.get("/execution-parameters")
def execution_parameters():
    return {
        "MaxConcurrentTransforms": 1,
        "BatchStrategy": "MULTI_RECORD",
        "MaxPayloadInMB": 6,
    }


if __name__ == "__main__":
    uvicorn.run("endpoint:app", host="0.0.0.0", port=8080, log_level="info")
