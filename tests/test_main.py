import main


def test_ai_process_without_api_key(monkeypatch):
    monkeypatch.setattr(main, "ai_client", None)
    assert "unavailable" in main.ai_process("Explain machine learning").lower()


def test_open_website_command(monkeypatch):
    opened = []
    monkeypatch.setattr(main.webbrowser, "open", opened.append)
    main.process_command("Open YouTube")
    assert opened == ["https://www.youtube.com/"]


def test_news_without_api_key_does_not_make_request(monkeypatch):
    spoken = []
    monkeypatch.setattr(main, "NEWS_API_KEY", None)
    monkeypatch.setattr(main, "speak", spoken.append)
    monkeypatch.setattr(main.requests, "get", lambda *a, **k: (_ for _ in ()).throw(AssertionError("unexpected request")))
    main.process_command("news")
    assert any("unavailable" in value.lower() for value in spoken)


def test_empty_command_is_handled(monkeypatch):
    spoken = []
    monkeypatch.setattr(main, "speak", spoken.append)
    main.process_command(" ")
    assert spoken == ["Please say a command."]



def test_ai_process_returns_model_response(monkeypatch):
    class FakeCompletions:
        @staticmethod
        def create(**kwargs):
            assert kwargs["model"] == main.OPENAI_MODEL
            assert kwargs["messages"][-1]["content"] == "Explain Python"
            return type(
                "Response",
                (),
                {
                    "choices": [
                        type(
                            "Choice",
                            (),
                            {"message": type("Message", (), {"content": "Python is a programming language."})()},
                        )()
                    ]
                },
            )()

    fake_client = type(
        "Client",
        (),
        {"chat": type("Chat", (), {"completions": FakeCompletions()})()},
    )()
    monkeypatch.setattr(main, "ai_client", fake_client)

    assert main.ai_process("Explain Python") == "Python is a programming language."


def test_ai_process_handles_api_error(monkeypatch):
    from openai import APIError

    class FakeCompletions:
        @staticmethod
        def create(**kwargs):
            raise APIError(
                message="temporary failure",
                request=None,
                body=None,
            )

    fake_client = type(
        "Client",
        (),
        {"chat": type("Chat", (), {"completions": FakeCompletions()})()},
    )()
    monkeypatch.setattr(main, "ai_client", fake_client)

    assert "issue processing" in main.ai_process("hello").lower()


def test_news_request_uses_timeout_and_speaks_headlines(monkeypatch):
    spoken = []
    captured = {}

    class FakeResponse:
        @staticmethod
        def raise_for_status():
            return None

        @staticmethod
        def json():
            return {"articles": [{"title": "Headline one"}, {"title": "Headline two"}]}

    def fake_get(url, **kwargs):
        captured.update(kwargs)
        return FakeResponse()

    monkeypatch.setattr(main, "NEWS_API_KEY", "test-key")
    monkeypatch.setattr(main.requests, "get", fake_get)
    monkeypatch.setattr(main, "speak", spoken.append)

    main.process_command("news")

    assert captured["timeout"] == 10
    assert spoken == ["Headline one", "Headline two"]
