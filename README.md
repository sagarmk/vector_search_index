# PDF Parser and FAISS Indexer
Main goal of this tool is to make documents searchable using FAISS index.
This application allows you to upload PDF files, parse their content, build a FAISS index based on the parsed content, and perform searches on the created index.

![alt text](/images/vectorsearch.png)

## Getting Started

These instructions will help you set up and run the application on your local machine.

### Prerequisites

You'll need to have the following tools installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. Clone this repository to your local machine:
    git clone https://github.com/yourusername/your-repository.git

2. Navigate to the project directory:
    cd your-repository

3. Build the Docker image:
    make build

4. Start the application:
    make up

5. Open your web browser and access the application at:'
    http://localhost:8501

6. To stop the application and remove the container, run:
    make down


## Usage

1. Upload one or more PDF files using the file uploader in the sidebar.

2. Enter a name for the new index and click the "Build and Save Index" button to parse the PDF files, build the index, and save it locally.

3. Select an existing index from the dropdown menu and click "Load Index" to load the selected index.

4. Enter a query in the text input field and click "Search" to perform a search on the loaded index.

5. The search results will be displayed as a list of paragraphs where the query was found.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.








