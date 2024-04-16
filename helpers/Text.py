class Text:
    def trim_text(self, texts: str) -> str:
        final_text = ""
        for i, text in enumerate(texts):
            if i <= 1900:
                final_text += text
        return final_text
