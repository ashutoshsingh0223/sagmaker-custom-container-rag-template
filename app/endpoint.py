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

    # Type of job, retrieve(for model endpoints)
    # or index(for batch transform jobs)
    job_type = manifest['job_type']
    # name for the job
    job_name = manifest['job_name']

    # A callback URL to update job status
    callback_url = manifest['callback_url']
    # Host for elasctic search , used here as vector DB.
    elastic_host = manifest["elastic_host"]

    t = processor.Processor(
                model_cache_dir="/opt/ml/model",
                elastic_host=elastic_host,
                environment=environment
            )

    if job_type == 'retrieve':
        query = manifest['query']
        docs = t.search(query)
        return {"docs": docs}
    else:
        st = time.time()
        import reader
        try:
            documents = manifest['documents']
            r = reader.DocReader(docs=documents)
            
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
