html_content_a_5layers = """
            <a>
                <p>a</p>
                <div>
                    <span>A</span>
                        <div>
                            <p>ba</p>
                        </div>
                        <div>
                            <p>ba</p>
                        </div>
                    <div>Ta</div>
                </div>
                <p>AA</p>
            </a>
            """

token_a = 'a'

html_content_a = """
            <a>
                <p>a</p>
                <div>
                    <span>A</span>
                    <div>Ta</div>
                </div>
                <p>AA</p>
            </a>
            """

html_content_a_double = """
            <a>
                <p>a</p>
                <div>
                    <span>A</span>
                    <div>Ta</div>
                </div>
                <p>AA</p>
                <p>a</p>
                <div>
                    <span>A</span>
                    <div>Ta</div>
                </div>
                <p>AA</p>
            </a>
            """

html_content_script = """
    <html>
        <head>
            <title>Sample Page</title>
            <script type="text/javascript">
                console.log('JavaScript code here');
            </script>
            <script type="application/json">
                {"key": "value"}
            </script>
            <script>
                console.log('Another script without a type attribute');
            </script>
        </head>
        <body>
            <p class="story">Once upon a time there were three little pigs...</p>
        </body>
    </html>

"""