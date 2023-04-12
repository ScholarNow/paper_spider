# PaperSpider

Crawling **prior** and **derivative** papers according to the origin paper.

## Requirements

- Python >= 3.8
- selenium==4.8.3

## Get Started

1. Install `Chrome` and `webdriver`.
2. Copy `.env_default` to `.env`, and fill `CHROME_DRIVER_PATH` with your `webdriver` path in `.env` file
3. Navigate to the project directory, and run the command to crawl papers:
    ```
    $ python main.py --query_file query.txt
    ```
    It will fetch the related papers according to the `query.txt`, you can also customize this file, just modify it.

    Alternatively, you can crawl a single paper use `--query`:
    ```
    $ python main.py --query BERT
    ```

Check the results in the `out/` folder, and the structure is like:
```
out
└── 04_05_18_08_25
    ├── 0.json
    ├── 1.json
    ├── 2.json
    ├── 3.json
    ├── 4.json
    ├── 5.json
    ├── 6.json
    └── query.txt
```
where `query.txt` is your queries if your specify the `--query_file query.txt`, and the `<i>.json` represents the related papers to the i-th item in the `query.txt` (`0.json` is the result for `--query xxx`).

The format of the json file is:
```json
{
    "origin_paper": {
        "title": "xxx",
        "authors": "<author1>, <author2>, ...",
        "link": "<semanticscholar link>",
        "publication": "<year>, <publication>",
        "year": 2019,
        "citations": 0,
        "abstract": ""
    },
    "prior_papers": [
        {
            "title": "xxx",
            "authors": "<author1>, <author2>, ...",
            "link": "<semanticscholar link>",
            "publication": "<year>, <publication>",
            "year": 2019,
            "citations": 0,
            "abstract": ""
        },
        // ...
    ],
    "derivative_papers": [
        {
            "title": "xxx",
            "authors": "<author1>, <author2>, ...",
            "link": "<semanticscholar link>",
            "publication": "<year>, <publication>",
            "year": 2019,
            "citations": 0,
            "abstract": ""
        },
        // ...
    ]
}
```

## Contribution

1. Install `pre-commit` package using `pip install pre-commit`
2. Install hooks using `pre-commit install`
3. Run `pre-commit run --all-files` to check all the file and `ruff` will automatically fix the style
4. Once you `git commit`, `pre-commit` also check the style of your changed files
5. Finally, you can create a pull-request (PR) to this repository.
