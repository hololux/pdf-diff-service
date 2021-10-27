# PDF-Diff

Azure Function wrapper for https://github.com/jnweiger/pdfcompare. It uses an adapted version of the `pdfcompare.py` file.

## Prerequsites

Requires Python Version 3.6 - 3.8.
Create a virtual environment in the root folder of the repository using:\
`python -m venv .venv`

You can deactivate it with:\
`deactivate`\
and activate it again with:\
`source .venv/bin/activate`

Install dependencies using:\
`python -m pip install -r requirements.txt`

To run the function locally outside of docker you need **pdftohtml** Version 0.74.0 or higher. (Not available on MacOS)

## Running the function locally from container

Create the image using:\
`docker build --tag <DOCKER_ID>/azurefunctionsimage:v1.0.0 .`

Run the container using:\
`docker run -p 8080:80 -it <docker_id>/azurefunctionsimage:v1.0.0`

## API specification

PDF-Diff is an HttpTrigger Azure function, which accepts POST requests with the following JSON schema as payload:

```
  {
    "pdfOld": <base64 string>,
    "pdfNew": <base64 string>
  }
```

- pdfOld: The original PDF file against which the the new one will be compared against
- pdfNew: The new version of the pdf file which will be used for the resulting annotated PDF

Both base64 inputs can be sent with or without the base64 header.

The API will return the following JSON:

```
{
  "changePdf": <base64 string>,
  "hasChanges": boolean
}
```

- changePdf: The pdfNew file with annotations on what has changed compared to the pdfOld file
- hasChanges: Indicates whether or not the two files have any differences
