
import gradio as gr

def greet(name):
    return f"Hello {name}!"


if __name__ == '__main__':
    # demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    # demo = gr.Interface(fn=greet, inputs="textbox", outputs="textbox", flagging_mode="never")

    # 1.
    # demo.launch()

    # 2. When share = True; This will generate a link which is run on Hugging face cloud so other's can use this.
    # It's something similar to Ngrok
    # demo.launch(share=True)

    # 3. Auto opens in browser, don't need to click the open to open.
    # demo.launch(inbrowser=True)

    # 4. Password to enter
    # demo.launch(inbrowser=True, auth=[("user", "password"), ("ak", "ak6")])

    # 5. script to force gradio to change the mode according to us. It's not working.
    # force_dark_mode = """
    # function refresh() {
    #     const url = new URL(window.location);
    #     if (url.searchParams.get('__theme') !== 'light') {
    #         url.searchParams.set('__theme', 'light');
    #         window.location.href = url.href;
    #     }
    # }
    # """
    # demo = gr.Interface(fn=greet, inputs="textbox", outputs="textbox", flagging_mode="never", js=force_dark_mode)
    # demo.launch()

    # 6. Let's do something different with gradio
    message_input = gr.Textbox(label="Your message: ", info="Enter your name", lines=7)
    message_output = gr.Textbox(label="Response: ", lines=8)

    demo = gr.Interface(
        fn=greet,
        inputs=[message_input],
        outputs=[message_output],
        examples=["Akhil", "Vamshi"],
        flagging_mode="never"
    )
    demo.launch(inbrowser=True)

    # 7.
