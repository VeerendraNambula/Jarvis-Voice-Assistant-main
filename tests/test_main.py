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
