main_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local RAG Solution</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        header {
            background-color: #2196f3;
            color: white;
            width: 100%;
            padding: 1.5em;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        main {
            margin: 2em;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            width: 90%;
            max-width: 800px;
            padding: 2em;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
            font-size: 1.1em;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        ul li {
            background-color: #2196f3;
            margin: 0.5em 0;
            padding: 1em;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        ul li a {
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
        }
        ul li:hover {
            background-color: #1976d2;
        }
        .material-icons {
            margin-right: 0.5em;
        }
    </style>
</head>
<body>
    <header>
        <h1>Local RAG Solution</h1>
    </header>
    <main>
        <p>If you need to chat directly with the model based on uploaded documents, please visit <a href="/chat">RAG Q&A</a> and upload files in the input area to start the conversation. (The uploaded data will not be retained after page refresh. If you want to persistently use and maintain a knowledge base, please create a knowledge base).</p>
        <p>If you need to create or update a knowledge base, please follow the steps: <a href="/upload_data">Upload Data</a>, <a href="/create_knowledge_base">Create Knowledge Base</a>, then select the knowledge base you want to use in the "Knowledge Base Selection" section of <a href="/chat">RAG Q&A</a>.</p>
        <p>If you need to perform Q&A based on an already created knowledge base, please visit <a href="/chat">RAG Q&A</a> and select your created knowledge base in the "Load Knowledge Base" section.</p>
        <ul>
            <li><a href="/upload_data"><span class="material-icons">cloud_upload</span> 1. Upload Data</a></li>
            <li><a href="/create_knowledge_base"><span class="material-icons">library_add</span> 2. Create Knowledge Base</a></li>
            <li><a href="/chat"><span class="material-icons">question_answer</span> 3. RAG Q&A</a></li>
        </ul>
    </main>
</body>
</html>"""

plain_html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>RAG Q&A</title>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
        .links-container {
            display: flex;
            justify-content: center; /* Center distribute child elements in container */
            list-style-type: none; /* Remove default list style */
            padding: 0; /* Remove default padding */
            margin: 0; /* Remove default margin */
        }
        .links-container li {
            margin: 0 5px; /* Add some space on left and right of each li element */
            padding: 10px 15px; /* Add padding */
            border: 1px solid #ccc; /* Add border */
            border-radius: 5px; /* Add rounded corners */
            background-color: #f9f9f9; /* Background color */
            transition: background-color 0.3s; /* Background color transition effect */
            display: flex; /* Use flex layout */
            align-items: center; /* Vertical center alignment */
            height: 50px; /* Set fixed height for consistency */
        }
        .links-container li:hover {
            background-color: #e0e0e0; /* Background color on hover */
        }
        .links-container a {
            text-decoration: none !important; /* Remove link underline */
            color: #333; /* Link color */
            font-family: Arial, sans-serif; /* Font */
            font-size: 14px; /* Font size */
            display: flex; /* Use flex layout */
            align-items: center; /* Vertical center alignment */
            height: 100%; /* Ensure link height matches parent element */
        }
        .material-icons {
            font-size: 20px; /* Icon size */
            margin-right: 8px; /* Spacing between icon and text */
            text-decoration: none; /* Ensure icon has no underline */
        }

        /* Dark mode styles */
        @media (prefers-color-scheme: dark) {
            .links-container li {
                background-color: #333; /* Background color in dark mode */
                border-color: #555; /* Border color in dark mode */
            }
            .links-container li:hover {
                background-color: #555; /* Background color on hover in dark mode */
            }
            .links-container a {
                color: #f9f9f9; /* Text color in dark mode */
            }
        }
        </style>
    </head>
    <body>
        <ul class="links-container">
            <li><a href="/"><span class="material-icons">home</span> Home</a></li>
            <li><a href="/upload_data"><span class="material-icons">cloud_upload</span> Upload Data</a></li>
            <li><a href="/create_knowledge_base"><span class="material-icons">library_add</span> Create Knowledge Base</a></li>
            <li><a href="/chat"><span class="material-icons">question_answer</span> RAG Q&A</a></li>
        </ul>
    </body>
</html>"""
