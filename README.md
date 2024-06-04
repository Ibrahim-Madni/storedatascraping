
# Project Readme

## Introduction

This document outlines the necessary steps for setting up and running the web scraping project that leverages Scrapy, Scrapy Splash, and Scrapy Pipeline along with Splash via Docker.

## Requirements

- Python installed
- Docker installed
- Windows or Linux operating system

## Installation Steps

### Step 1: Install Python Packages

To install the required Python packages, open your terminal or command prompt and execute the following commands:

```bash
pip install scrapy
pip install scrapy-splash
```
### Step 2: Set Up Docker
If you haven't installed Docker yet, you can download it from the [official website](https://www.docker.com/products/docker-desktop/).

## Pulling Splash Image
Execute the following command to pull the Splash Docker image:

```bash
docker pull scrapinghub/splash
```

## Running Splash
Run the Splash container with the following command:

### For Windows (Powershell):

```bash
docker run -it -p 8050:8050 --rm scrapinghub/splash
```
### For Linux:

```bash
sudo docker run -it -p 8050:8050 --rm scrapinghub/splash
```

### Step 3: Run Scrapy Spider
After the Docker container is up and running, navigate to your StoreData directory:

```bash
cd "\store-data-scraping\StoreData"
```
Run the Scrapy spider with the following command:

```bash
scrapy crawl datastore-spider
```
## Additional Notes
Make sure Docker is running before you attempt to pull or run the Splash image.
Ensure your Scrapy spider (datastore-spider) is correctly placed within the StoreData directory.

## Troubleshooting
If you encounter issues, refer to the respective documentations:

- [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
- [Scrapy-Splash Documentation](https://github.com/scrapy-plugins/scrapy-splash)
- [Docker Documentation](https://docs.docker.com/)

Feel free to contribute or report issues to this project.

Thank you for using this project. For further questions or concerns, please refer to the project maintainers.# storedatascraping
