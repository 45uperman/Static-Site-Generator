import unittest
from convertable_document import ConvertableDocument

class TestFullConversion(unittest.TestCase):
    def test_markdown_to_html(self):
        html_img = lambda html_img: f'<img src="{html_img["link"]}" alt="{html_img["text"]}">'
        md_img = lambda md_img: f'![{md_img["text"]}]({md_img["link"]})'
        html_link = lambda html_link: f'<a href="{html_link["link"]}">{html_link["text"]}</a>'
        md_link = lambda md_link: f'[{md_link["text"]}]({md_link["link"]})'
        test_image = {"link": "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png", "text": "image"}
        test_link = {"link": "https://boot.dev", "text": "link"}
        test_heading_1 = "# This is heading 1!"
        test_heading_2 = "## This is heading 2!"
        test_heading_6 = "###### I got lazy..."
        test_paragraph = f"This is **text** with an *italic* word and a `code snippet` and an {md_img(test_image)} and a {md_link(test_link)}."
        test_unordered_list = f"* This is an\n* **unordered** *list* with\n* a {md_link(test_link)}\n* *and* an {md_img(test_image)}"
        test_ordered_list = f"1. This is an\n2. **ordered** *list* with\n3. a {md_link(test_link)}\n4. *and* an {md_img(test_image)}"
        test_code = "```\nThis is some code!\nBeep boop!\nHello world!\n```"
        test_quote = "> This is a **quote.**\n> I *said* this.\n> **Meep.** **Morp.**"
        test_markdown = f"{test_heading_1}\n\n{test_heading_2}\n\n{test_heading_6}\n\n{test_paragraph}\n\n{test_unordered_list}\n\n{test_ordered_list}\n\n{test_code}\n\n{test_quote}"
        html_headings = "<h1>This is heading 1!</h1><h2>This is heading 2!</h2><h6>I got lazy...</h6>"
        html_paragraph = f"<p>This is <b>text</b> with an <i>italic</i> word and a <code>code snippet</code> and an {html_img(test_image)} and a {html_link(test_link)}.</p>"
        html_unordered_list = f"<ul><li>This is an</li><li><b>unordered</b> <i>list</i> with</li><li>a {html_link(test_link)}</li><li><i>and</i> an {html_img(test_image)}</li></ul>"
        html_ordered_list = f"<ol><li>This is an</li><li><b>ordered</b> <i>list</i> with</li><li>a {html_link(test_link)}</li><li><i>and</i> an {html_img(test_image)}</li></ol>"
        html_code = "<pre><code>This is some code!\nBeep boop!\nHello world!</code></pre>"
        html_quote = "<blockquote>This is a <b>quote.</b> I <i>said</i> this. <b>Meep.</b> <b>Morp.</b></blockquote>"
        expected_html = f"<div>{html_headings}{html_paragraph}{html_unordered_list}{html_ordered_list}{html_code}{html_quote}</div>"
        test_document = ConvertableDocument(test_markdown)
        self.assertEqual(test_document.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()

