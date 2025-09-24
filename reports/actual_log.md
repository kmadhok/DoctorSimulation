(doctor_env) kanumadhok@Kanus-MacBook-Pro DoctorSimulation % python app.py --port 8001
2025-09-22 21:43:38,717 - utils.database - INFO - Current database version: 3, Target version: 2
2025-09-22 21:43:38,718 - utils.database - INFO - Database initialized successfully
2025-09-22 21:43:38,719 - utils.medical_validation - INFO - Successfully loaded medical knowledge from /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/medical_knowledge.json
2025-09-22 21:43:38,719 - utils.medical_validation - INFO - MedicalValidationSystem initialized with 7 specialties and 43 symptoms
2025-09-22 21:43:38,719 - utils.ai_case_generator - INFO - Medical validation system initialized successfully
21:43:39 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:39,447 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:39 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:39,448 - LiteLLM - DEBUG - Creating AiohttpTransport...
2025-09-22 21:43:39,453 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:43:39,454 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
2025-09-22 21:43:39,458 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:43:39,458 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
2025-09-22 21:43:39,462 - httpcore.connection - DEBUG - connect_tcp.started host='raw.githubusercontent.com' port=443 local_address=None timeout=5 socket_options=None
2025-09-22 21:43:39,478 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x10553ea10>
2025-09-22 21:43:39,478 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x1051230b0> server_hostname='raw.githubusercontent.com' timeout=5
2025-09-22 21:43:39,495 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x10554cd90>
2025-09-22 21:43:39,495 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'GET']>
2025-09-22 21:43:39,495 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:43:39,495 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'GET']>
2025-09-22 21:43:39,495 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:43:39,495 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'GET']>
2025-09-22 21:43:39,519 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Connection', b'keep-alive'), (b'Content-Length', b'39550'), (b'Cache-Control', b'max-age=300'), (b'Content-Security-Policy', b"default-src 'none'; style-src 'unsafe-inline'; sandbox"), (b'Content-Type', b'text/plain; charset=utf-8'), (b'ETag', b'W/"13edc3f947d0d6569673617266d74cb1c5feb383cf57390dd7f54ca52a544703"'), (b'Strict-Transport-Security', b'max-age=31536000'), (b'X-Content-Type-Options', b'nosniff'), (b'X-Frame-Options', b'deny'), (b'X-XSS-Protection', b'1; mode=block'), (b'X-GitHub-Request-Id', b'67B5:9524B:FD946:150B10:68D1DDE5'), (b'Content-Encoding', b'gzip'), (b'Accept-Ranges', b'bytes'), (b'Date', b'Tue, 23 Sep 2025 02:43:39 GMT'), (b'Via', b'1.1 varnish'), (b'X-Served-By', b'cache-chi-kigq8000088-CHI'), (b'X-Cache', b'HIT'), (b'X-Cache-Hits', b'1'), (b'X-Timer', b'S1758595420.507402,VS0,VE9'), (b'Vary', b'Authorization,Accept-Encoding'), (b'Access-Control-Allow-Origin', b'*'), (b'Cross-Origin-Resource-Policy', b'cross-origin'), (b'X-Fastly-Request-ID', b'728516bb72f76354611799c5e34feb64a57e0f79'), (b'Expires', b'Tue, 23 Sep 2025 02:48:39 GMT'), (b'Source-Age', b'18')])
2025-09-22 21:43:39,520 - httpx - INFO - HTTP Request: GET https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json "HTTP/1.1 200 OK"
2025-09-22 21:43:39,520 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'GET']>
2025-09-22 21:43:39,527 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:43:39,527 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:43:39,527 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:43:39,528 - httpcore.connection - DEBUG - close.started
2025-09-22 21:43:39,528 - httpcore.connection - DEBUG - close.complete
21:43:39 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:39,733 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:39 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:39,733 - LiteLLM - DEBUG - Creating AiohttpTransport...
2025-09-22 21:43:39,733 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:43:39,734 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
21:43:39 - LiteLLM:DEBUG: litellm_logging.py:168 - [Non-Blocking] Unable to import GenericAPILogger - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
2025-09-22 21:43:39,751 - LiteLLM - DEBUG - [Non-Blocking] Unable to import GenericAPILogger - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
21:43:39 - LiteLLM:DEBUG: transformation.py:17 - [Non-Blocking] Unable to import _ENTERPRISE_ResponsesSessionHandler - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
2025-09-22 21:43:39,889 - LiteLLM - DEBUG - [Non-Blocking] Unable to import _ENTERPRISE_ResponsesSessionHandler - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
21:43:39 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:39,891 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:39 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:39,891 - LiteLLM - DEBUG - Creating AiohttpTransport...
21:43:39 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:39,893 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:39 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:39,893 - LiteLLM - DEBUG - Creating AiohttpTransport...
2025-09-22 21:43:40,293 - __main__ - INFO - Reports directory ensured at /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports
2025-09-22 21:43:40,294 - utils.database - INFO - Current database version: 3, Target version: 2
2025-09-22 21:43:40,294 - utils.database - INFO - Database initialized successfully
2025-09-22 21:43:40,297 - __main__ - INFO - GROQ_API_KEY found - length: 56
2025-09-22 21:43:40,298 - __main__ - INFO - Starting Flask app on 0.0.0.0:8001
 * Serving Flask app 'app'
 * Debug mode: on
2025-09-22 21:43:40,510 - werkzeug - INFO - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8001
 * Running on http://192.168.1.239:8001
2025-09-22 21:43:40,510 - werkzeug - INFO - Press CTRL+C to quit
2025-09-22 21:43:40,513 - werkzeug - INFO -  * Restarting with stat
2025-09-22 21:43:40,911 - utils.database - INFO - Current database version: 3, Target version: 2
2025-09-22 21:43:40,911 - utils.database - INFO - Database initialized successfully
2025-09-22 21:43:40,912 - utils.medical_validation - INFO - Successfully loaded medical knowledge from /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/medical_knowledge.json
2025-09-22 21:43:40,912 - utils.medical_validation - INFO - MedicalValidationSystem initialized with 7 specialties and 43 symptoms
2025-09-22 21:43:40,912 - utils.ai_case_generator - INFO - Medical validation system initialized successfully
21:43:42 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:42,914 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:42 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:42,915 - LiteLLM - DEBUG - Creating AiohttpTransport...
2025-09-22 21:43:42,921 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:43:42,922 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
2025-09-22 21:43:42,928 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:43:42,928 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
2025-09-22 21:43:42,933 - httpcore.connection - DEBUG - connect_tcp.started host='raw.githubusercontent.com' port=443 local_address=None timeout=5 socket_options=None
2025-09-22 21:43:42,954 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x10b09cd50>
2025-09-22 21:43:42,955 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x10aa77140> server_hostname='raw.githubusercontent.com' timeout=5
2025-09-22 21:43:43,087 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x10b09cf90>
2025-09-22 21:43:43,087 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'GET']>
2025-09-22 21:43:43,087 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:43:43,087 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'GET']>
2025-09-22 21:43:43,088 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:43:43,088 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'GET']>
2025-09-22 21:43:43,100 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Connection', b'keep-alive'), (b'Content-Length', b'39550'), (b'Cache-Control', b'max-age=300'), (b'Content-Security-Policy', b"default-src 'none'; style-src 'unsafe-inline'; sandbox"), (b'Content-Type', b'text/plain; charset=utf-8'), (b'ETag', b'W/"13edc3f947d0d6569673617266d74cb1c5feb383cf57390dd7f54ca52a544703"'), (b'Strict-Transport-Security', b'max-age=31536000'), (b'X-Content-Type-Options', b'nosniff'), (b'X-Frame-Options', b'deny'), (b'X-XSS-Protection', b'1; mode=block'), (b'X-GitHub-Request-Id', b'67B5:9524B:FD946:150B10:68D1DDE5'), (b'Content-Encoding', b'gzip'), (b'Accept-Ranges', b'bytes'), (b'Date', b'Tue, 23 Sep 2025 02:43:43 GMT'), (b'Via', b'1.1 varnish'), (b'X-Served-By', b'cache-chi-kigq8000087-CHI'), (b'X-Cache', b'HIT'), (b'X-Cache-Hits', b'3'), (b'X-Timer', b'S1758595423.097053,VS0,VE0'), (b'Vary', b'Authorization,Accept-Encoding'), (b'Access-Control-Allow-Origin', b'*'), (b'Cross-Origin-Resource-Policy', b'cross-origin'), (b'X-Fastly-Request-ID', b'4ff15c02b3f74e050bf79a070db430b19f41958f'), (b'Expires', b'Tue, 23 Sep 2025 02:48:43 GMT'), (b'Source-Age', b'22')])
2025-09-22 21:43:43,102 - httpx - INFO - HTTP Request: GET https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json "HTTP/1.1 200 OK"
2025-09-22 21:43:43,102 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'GET']>
2025-09-22 21:43:43,131 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:43:43,131 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:43:43,131 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:43:43,131 - httpcore.connection - DEBUG - close.started
2025-09-22 21:43:43,131 - httpcore.connection - DEBUG - close.complete
21:43:43 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:43,330 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:43 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:43,330 - LiteLLM - DEBUG - Creating AiohttpTransport...
2025-09-22 21:43:43,330 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:43:43,330 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
21:43:43 - LiteLLM:DEBUG: litellm_logging.py:168 - [Non-Blocking] Unable to import GenericAPILogger - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
2025-09-22 21:43:43,348 - LiteLLM - DEBUG - [Non-Blocking] Unable to import GenericAPILogger - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
21:43:43 - LiteLLM:DEBUG: transformation.py:17 - [Non-Blocking] Unable to import _ENTERPRISE_ResponsesSessionHandler - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
2025-09-22 21:43:43,458 - LiteLLM - DEBUG - [Non-Blocking] Unable to import _ENTERPRISE_ResponsesSessionHandler - LiteLLM Enterprise Feature - No module named 'litellm_enterprise'
21:43:43 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:43,460 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:43 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:43,460 - LiteLLM - DEBUG - Creating AiohttpTransport...
21:43:43 - LiteLLM:DEBUG: http_handler.py:530 - Using AiohttpTransport...
2025-09-22 21:43:43,461 - LiteLLM - DEBUG - Using AiohttpTransport...
21:43:43 - LiteLLM:DEBUG: http_handler.py:554 - Creating AiohttpTransport...
2025-09-22 21:43:43,461 - LiteLLM - DEBUG - Creating AiohttpTransport...
2025-09-22 21:43:43,714 - __main__ - INFO - Reports directory ensured at /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports
2025-09-22 21:43:43,715 - utils.database - INFO - Current database version: 3, Target version: 2
2025-09-22 21:43:43,715 - utils.database - INFO - Database initialized successfully
2025-09-22 21:43:43,718 - __main__ - INFO - GROQ_API_KEY found - length: 56
2025-09-22 21:43:43,719 - __main__ - INFO - Starting Flask app on 0.0.0.0:8001
2025-09-22 21:43:43,737 - werkzeug - WARNING -  * Debugger is active!
2025-09-22 21:43:43,746 - werkzeug - INFO -  * Debugger PIN: 932-825-516
2025-09-22 21:43:50,295 - __main__ - DEBUG - Request: GET /
2025-09-22 21:43:50,295 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,296 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,296 - __main__ - INFO - Serving index page
2025-09-22 21:43:50,302 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET / HTTP/1.1" 200 -
2025-09-22 21:43:50,370 - __main__ - DEBUG - Request: GET /static/css/style.css
2025-09-22 21:43:50,370 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: text/css,*/*;q=0.1
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: style
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,371 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,373 - __main__ - DEBUG - Request: GET /static/css/multi-agent.css
2025-09-22 21:43:50,373 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: text/css,*/*;q=0.1
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: style
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,374 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,376 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET /static/css/style.css HTTP/1.1" 200 -
2025-09-22 21:43:50,377 - __main__ - DEBUG - Request: GET /static/vad-model/ort.min.js
2025-09-22 21:43:50,378 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET /static/css/multi-agent.css HTTP/1.1" 200 -
2025-09-22 21:43:50,379 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: script
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,381 - __main__ - DEBUG - Request: GET /static/vad-model/bundle.min.js
2025-09-22 21:43:50,382 - __main__ - DEBUG - Request: GET /static/js/main.js
2025-09-22 21:43:50,382 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,383 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: script
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,383 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: script
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,384 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,384 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,385 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET /static/vad-model/ort.min.js HTTP/1.1" 200 -
2025-09-22 21:43:50,386 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET /static/vad-model/bundle.min.js HTTP/1.1" 200 -
2025-09-22 21:43:50,386 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET /static/js/main.js HTTP/1.1" 200 -
2025-09-22 21:43:50,486 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:43:50,486 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,486 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,488 - __main__ - DEBUG - Request: GET /api/personas
2025-09-22 21:43:50,488 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:50,488 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:50,489 - __main__ - INFO - Listing available personas
2025-09-22 21:43:50,489 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET /api/personas HTTP/1.1" 200 -
2025-09-22 21:43:50,492 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:50] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:43:54,603 - __main__ - DEBUG - Request: POST /api/multi-agent/create
2025-09-22 21:43:54,603 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Content-Length: 55
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Content-Type: application/json
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Origin: http://localhost:8001
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:54,603 - __main__ - DEBUG - Body: b'{"agent_ids":["negative_debater","optimistic_debater"]}'
2025-09-22 21:43:54,613 - utils.crew_agents - INFO - Added agent Sage – The Thoughtful Skeptic to conversation
2025-09-22 21:43:54,618 - utils.crew_agents - INFO - Added agent Hope – The Optimistic Voice to conversation
2025-09-22 21:43:54,620 - utils.database - DEBUG - Created conversation 99: Conference Call: Sage – The Thoughtful Skeptic, Hope – The Optimistic Voice
2025-09-22 21:43:54,622 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: conversation_type
2025-09-22 21:43:54,622 - utils.database - DEBUG - Storing JSON data for conversation 99, key: active_agents
2025-09-22 21:43:54,623 - utils.database - DEBUG - Successfully stored json data for conversation 99, key: active_agents
2025-09-22 21:43:54,623 - __main__ - INFO - Created multi-agent conversation with agents: ['Sage – The Thoughtful Skeptic', 'Hope – The Optimistic Voice']
2025-09-22 21:43:54,624 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:54] "POST /api/multi-agent/create HTTP/1.1" 200 -
2025-09-22 21:43:58,790 - __main__ - DEBUG - Request: GET /static/vad-model/ort-wasm-simd-threaded.jsep.mjs
2025-09-22 21:43:58,790 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Origin: http://localhost:8001
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: script
Referer: http://localhost:8001/static/vad-model/ort.min.js
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:58,790 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:58,791 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:58] "GET /static/vad-model/ort-wasm-simd-threaded.jsep.mjs HTTP/1.1" 200 -
2025-09-22 21:43:58,798 - __main__ - DEBUG - Request: GET /static/vad-model/ort-wasm-simd-threaded.jsep.wasm
2025-09-22 21:43:58,799 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:43:58,799 - __main__ - DEBUG - Body: b''
2025-09-22 21:43:58,800 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:43:58] "GET /static/vad-model/ort-wasm-simd-threaded.jsep.wasm HTTP/1.1" 200 -
2025-09-22 21:44:03,479 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:03,479 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:03,481 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:03,482 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:03,482 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:03,482 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:03,482 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:03,484 - utils.database - DEBUG - Retrieved 2 data items for conversation 99
2025-09-22 21:44:03,484 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type']
2025-09-22 21:44:03,486 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:03,486 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:03,487 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:03,487 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type']
2025-09-22 21:44:03,487 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:03,487 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:03,487 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type"], "timestamp": "2025-09-22T21:44:03.487281"}
2025-09-22 21:44:03,487 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:03,487 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:03,489 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:03,490 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:03,490 - __main__ - DEBUG - Read 67628 bytes from audio file
2025-09-22 21:44:03,490 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:03,529 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:03,790 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:03,793 - __main__ - DEBUG - Transcription successful: 'Hello.'
2025-09-22 21:44:03,794 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 0 previous messages
2025-09-22 21:44:03,796 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:03,797 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:03,814 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:03,851 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:03,852 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:03,860 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x11838e850>
2025-09-22 21:44:03,860 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x118359910> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:03,870 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183e6d50>
2025-09-22 21:44:03,871 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:03,871 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:03,871 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:03,871 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:03,871 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:04,217 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:03 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299699'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'60.2ms'), (b'x-request-id', b'req_01k5t79v6kerp9grb4c2wdapde'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=bnyQhGr6cflCovbgIIYtI41Ec4O7.SH03fJq3Aji1ck-1758595443-1.0.1.1-.WJMaP4SIhkxPRpZ4zO_KMDs2bh6pVJ3lrWmH3HYLv71xbWKy9uAl2XfteM5v3cNsUkU_TWlocz0mVYiGGbS0NzOyL5yH4GpZCOmHdJiTDM; path=/; expires=Tue, 23-Sep-25 03:14:03 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b2b43b844f3f-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:04,219 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:04,220 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:04,220 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:04,220 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:04,221 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:04,221 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:03 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299699', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '60.2ms', 'x-request-id': 'req_01k5t79v6kerp9grb4c2wdapde', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=bnyQhGr6cflCovbgIIYtI41Ec4O7.SH03fJq3Aji1ck-1758595443-1.0.1.1-.WJMaP4SIhkxPRpZ4zO_KMDs2bh6pVJ3lrWmH3HYLv71xbWKy9uAl2XfteM5v3cNsUkU_TWlocz0mVYiGGbS0NzOyL5yH4GpZCOmHdJiTDM; path=/; expires=Tue, 23-Sep-25 03:14:03 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b2b43b844f3f-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:04,235 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:04,235 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:04,235 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:04,235 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'Hello....'
2025-09-22 21:44:04,235 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:04,238 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:04,539 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:04,616 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:04,616 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:04,617 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 9070 bytes
2025-09-22 21:44:04,618 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:04,619 - __main__ - DEBUG - Speech audio generated successfully: 9070 bytes
2025-09-22 21:44:04,619 - __main__ - DEBUG - Base64 audio size: 12096
2025-09-22 21:44:04,621 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
2025-09-22 21:44:04,622 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:04,623 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:04] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:04,649 - __main__ - DEBUG - Request: GET /favicon.ico
2025-09-22 21:44:04,649 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: image
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:04,649 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:04,649 - __main__ - WARNING - 404 error: 404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. - Path: /favicon.ico, Method: GET
2025-09-22 21:44:04,650 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:04] "GET /favicon.ico HTTP/1.1" 404 -
2025-09-22 21:44:05,769 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:05,770 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:05,770 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:05,775 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:05] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:10,768 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:10,768 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:10,770 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:10,770 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:10,770 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:10,771 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:10,771 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:10,772 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:44:10,772 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:10,772 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:10,773 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:10,773 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:10,773 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:10,773 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:10,773 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:10,773 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:44:10,773 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:44:10.773373"}
2025-09-22 21:44:10,773 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:10,773 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:10,774 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:10,774 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:10,775 - __main__ - DEBUG - Read 82988 bytes from audio file
2025-09-22 21:44:10,775 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:10,778 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:11,141 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:11,143 - __main__ - DEBUG - Transcription successful: 'How are you doing today?'
2025-09-22 21:44:11,145 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 2 previous messages
2025-09-22 21:44:11,146 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:11,147 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:11,163 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:11,163 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:11,164 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:11,174 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f5910>
2025-09-22 21:44:11,174 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x118359d00> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:11,190 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f59d0>
2025-09-22 21:44:11,190 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:11,191 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:11,191 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:11,191 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:11,191 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:11,403 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:11 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299682'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'63.6ms'), (b'x-request-id', b'req_01k5t7a2b4et5ax2rnkddtk482'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=jmol2aHHtFtIjC6uWPs0RcKv_bAvGfgkfNFmpenTtbU-1758595451-1.0.1.1-_U.jL42ygS9VsETn7wln12r4S0i9IWvFDuMrRPRDqcq5chDwn8GKhzuh..tjeVeIS_tcH_pfxvRJbKPqK3B_QgoDSAYZojUDvHU18xBr2kg; path=/; expires=Tue, 23-Sep-25 03:14:11 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b2e1fa51b648-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:11,404 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:11,404 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:11,405 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:11,405 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:11,405 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:11,405 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:11 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299682', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '63.6ms', 'x-request-id': 'req_01k5t7a2b4et5ax2rnkddtk482', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=jmol2aHHtFtIjC6uWPs0RcKv_bAvGfgkfNFmpenTtbU-1758595451-1.0.1.1-_U.jL42ygS9VsETn7wln12r4S0i9IWvFDuMrRPRDqcq5chDwn8GKhzuh..tjeVeIS_tcH_pfxvRJbKPqK3B_QgoDSAYZojUDvHU18xBr2kg; path=/; expires=Tue, 23-Sep-25 03:14:11 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b2e1fa51b648-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:11,413 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:11,414 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:11,414 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:11,414 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'I'm not feeling well....'
2025-09-22 21:44:11,414 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:11,418 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:11,576 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:11,695 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:11,696 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:11,696 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 13102 bytes
2025-09-22 21:44:11,696 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:11,697 - __main__ - DEBUG - Speech audio generated successfully: 13102 bytes
2025-09-22 21:44:11,697 - __main__ - DEBUG - Base64 audio size: 17472
2025-09-22 21:44:11,697 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:11,698 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:11] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:13,335 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:13,336 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:13,337 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:13,340 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:13] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:17,400 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:17,400 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:17,402 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:17,402 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:17,402 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:17,402 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:17,402 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:17,404 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:44:17,405 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:17,406 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:17,406 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:17,406 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:17,407 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:17,407 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:17,407 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:17,407 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:44:17,407 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:44:17.407676"}
2025-09-22 21:44:17,407 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:17,407 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:17,411 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:17,411 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:17,411 - __main__ - DEBUG - Read 73772 bytes from audio file
2025-09-22 21:44:17,411 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:17,416 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:17,704 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:17,706 - __main__ - DEBUG - Transcription successful: 'Tell me more.'
2025-09-22 21:44:17,707 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 4 previous messages
2025-09-22 21:44:17,709 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:17,710 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:17,725 - httpcore.connection - DEBUG - close.started
2025-09-22 21:44:17,725 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:44:17,729 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:17,729 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:17,730 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:17,736 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f1210>
2025-09-22 21:44:17,737 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x118359eb0> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:17,751 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f1d90>
2025-09-22 21:44:17,751 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:17,751 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:17,751 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:17,752 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:17,752 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:17,984 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:17 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299664'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'67.2ms'), (b'x-request-id', b'req_01k5t7a8qsej0s8zdcnf1mn6dy'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=7rKscxG5wKigsCt6py.n4RD9bjWkzzSugp4komHqVwY-1758595457-1.0.1.1-jKhzRQm09GsalUvjKpG36vc5diKbYZ7vXBZpAx6ZKCiNc2SUoRZ8sCMOuYFmkiNHjuSLZ8E.lo3gZ6bTlHgUcjejc0BF9N8b_4SotbWnh9Q; path=/; expires=Tue, 23-Sep-25 03:14:17 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b30af9e40d5b-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:17,985 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:17,986 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:17,986 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:17,986 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:17,986 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:17,987 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:17 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299664', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '67.2ms', 'x-request-id': 'req_01k5t7a8qsej0s8zdcnf1mn6dy', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=7rKscxG5wKigsCt6py.n4RD9bjWkzzSugp4komHqVwY-1758595457-1.0.1.1-jKhzRQm09GsalUvjKpG36vc5diKbYZ7vXBZpAx6ZKCiNc2SUoRZ8sCMOuYFmkiNHjuSLZ8E.lo3gZ6bTlHgUcjejc0BF9N8b_4SotbWnh9Q; path=/; expires=Tue, 23-Sep-25 03:14:17 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b30af9e40d5b-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:17,997 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:17,997 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:17,997 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:17,997 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'I have a headache and my body aches....'
2025-09-22 21:44:17,998 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:18,002 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:18,213 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:18,502 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:18,502 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:18,502 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 21166 bytes
2025-09-22 21:44:18,503 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:18,504 - __main__ - DEBUG - Speech audio generated successfully: 21166 bytes
2025-09-22 21:44:18,504 - __main__ - DEBUG - Base64 audio size: 28224
2025-09-22 21:44:18,505 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:18,506 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:18] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:21,162 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:21,163 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:21,163 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:21,167 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:21] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:23,917 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:23,918 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:23,919 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:23,919 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:23,919 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:23,920 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:23,920 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:23,922 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:44:23,922 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:23,923 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:23,923 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:23,924 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:23,924 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:23,924 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:23,924 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:23,924 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:44:23,924 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:44:23.924669"}
2025-09-22 21:44:23,924 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:23,924 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:23,927 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:23,927 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:23,927 - __main__ - DEBUG - Read 79916 bytes from audio file
2025-09-22 21:44:23,927 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:23,932 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:24,194 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:24,196 - __main__ - DEBUG - Transcription successful: 'That's no fun.'
2025-09-22 21:44:24,197 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 6 previous messages
2025-09-22 21:44:24,198 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:24,201 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:24,222 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}, {'role': 'assistant', 'content': 'I have a headache and my body aches.'}, {'role': 'user', 'content': "That's no fun."}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:24,223 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:24,223 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:24,233 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118d93910>
2025-09-22 21:44:24,249 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x118359400> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:24,263 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f47d0>
2025-09-22 21:44:24,264 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:24,264 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:24,264 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:24,264 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:24,264 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:24,368 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:24 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299642'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'71.6ms'), (b'x-request-id', b'req_01k5t7af3aejpbx7z1fev28p2m'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=fiAJSA3K7T8WQZD_qxG4lbKOf1hskZu7S3GeMr6C554-1758595464-1.0.1.1-0YfXbdY_2ioXyy9tD6vw09fkWlVTwZtXPZMdbY4TZ2pIfRRdT7PxrDUOYBLDJsW6TRb2N_82C4.J_2xu.meHbb40S8zKlDHQiUUz_Em8_us; path=/; expires=Tue, 23-Sep-25 03:14:24 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b333bd8f1116-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:24,370 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:24,370 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:24,371 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:24,371 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:24,371 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:24,372 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:24 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299642', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '71.6ms', 'x-request-id': 'req_01k5t7af3aejpbx7z1fev28p2m', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=fiAJSA3K7T8WQZD_qxG4lbKOf1hskZu7S3GeMr6C554-1758595464-1.0.1.1-0YfXbdY_2ioXyy9tD6vw09fkWlVTwZtXPZMdbY4TZ2pIfRRdT7PxrDUOYBLDJsW6TRb2N_82C4.J_2xu.meHbb40S8zKlDHQiUUz_Em8_us; path=/; expires=Tue, 23-Sep-25 03:14:24 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b333bd8f1116-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:24,380 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:24,381 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:24,381 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:24,381 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'No....'
2025-09-22 21:44:24,381 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:24,384 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:24,604 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:24,797 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:24,797 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:24,797 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 13102 bytes
2025-09-22 21:44:24,798 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:24,799 - __main__ - DEBUG - Speech audio generated successfully: 13102 bytes
2025-09-22 21:44:24,799 - __main__ - DEBUG - Base64 audio size: 17472
2025-09-22 21:44:24,799 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:24,800 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:24] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:26,444 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:26,445 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:26,445 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:26,449 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:26] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:32,849 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:32,851 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:32,853 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:32,853 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:32,853 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:32,853 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:32,853 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:32,854 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:44:32,855 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:32,855 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:32,855 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:32,856 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:32,856 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:32,856 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:32,856 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:32,856 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:44:32,857 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:44:32.856857"}
2025-09-22 21:44:32,857 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:32,857 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:32,860 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:32,861 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:32,861 - __main__ - DEBUG - Read 86060 bytes from audio file
2025-09-22 21:44:32,861 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:32,865 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:33,151 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:33,153 - __main__ - DEBUG - Transcription successful: 'Is there anyone else there?'
2025-09-22 21:44:33,154 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 8 previous messages
2025-09-22 21:44:33,155 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:33,156 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:33,177 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}, {'role': 'assistant', 'content': 'I have a headache and my body aches.'}, {'role': 'user', 'content': "That's no fun."}, {'role': 'assistant', 'content': 'No.'}, {'role': 'user', 'content': 'Is there anyone else there?'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:33,178 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:33,178 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:33,190 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118357510>
2025-09-22 21:44:33,190 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x118359370> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:33,209 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118357ed0>
2025-09-22 21:44:33,209 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:33,209 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:33,209 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:33,210 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:33,210 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:33,376 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:33 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299626'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'74.8ms'), (b'x-request-id', b'req_01k5t7aqv8ekq8x8v5hxmxca99'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=0QZ807zqiHl_TuKHkS4VzDOZN3KJTRNIaGGXHjXUD2s-1758595473-1.0.1.1-TbFynxx_1dr7o3qygOltcRGpkeukTsSu6GrMJI1RhQ_JZoqocujTZhVBh3quASh0AY.IVZK0BLDwYJ1ObQTI2p.R4z_FheKK1qC4ylR72Yw; path=/; expires=Tue, 23-Sep-25 03:14:33 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b36b9f232b4b-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:33,377 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:33,377 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:33,378 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:33,378 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:33,378 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:33,378 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:33 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299626', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '74.8ms', 'x-request-id': 'req_01k5t7aqv8ekq8x8v5hxmxca99', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=0QZ807zqiHl_TuKHkS4VzDOZN3KJTRNIaGGXHjXUD2s-1758595473-1.0.1.1-TbFynxx_1dr7o3qygOltcRGpkeukTsSu6GrMJI1RhQ_JZoqocujTZhVBh3quASh0AY.IVZK0BLDwYJ1ObQTI2p.R4z_FheKK1qC4ylR72Yw; path=/; expires=Tue, 23-Sep-25 03:14:33 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b36b9f232b4b-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:33,384 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:33,384 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:33,384 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:33,384 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'My wife is with me....'
2025-09-22 21:44:33,384 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:33,386 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:33,504 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:33,621 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:33,622 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:33,622 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 13102 bytes
2025-09-22 21:44:33,622 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:33,623 - __main__ - DEBUG - Speech audio generated successfully: 13102 bytes
2025-09-22 21:44:33,623 - __main__ - DEBUG - Base64 audio size: 17472
2025-09-22 21:44:33,624 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:33,624 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:33] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:35,254 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:35,255 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:35,255 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:35,258 - httpcore.connection - DEBUG - close.started
2025-09-22 21:44:35,258 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:44:35,262 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:35] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:38,318 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:38,318 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:38,320 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:38,320 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:38,320 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:38,320 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:38,320 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:38,322 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:44:38,322 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:38,323 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:38,324 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:38,324 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:38,324 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:38,324 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:38,324 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:38,325 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:44:38,325 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:44:38.325280"}
2025-09-22 21:44:38,325 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:38,325 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:38,328 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:38,329 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:38,329 - __main__ - DEBUG - Read 92204 bytes from audio file
2025-09-22 21:44:38,329 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:38,334 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:38,628 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:38,629 - __main__ - DEBUG - Transcription successful: 'What is your wife's name?'
2025-09-22 21:44:38,629 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 10 previous messages
2025-09-22 21:44:38,630 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:38,630 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:38,640 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}, {'role': 'assistant', 'content': 'I have a headache and my body aches.'}, {'role': 'user', 'content': "That's no fun."}, {'role': 'assistant', 'content': 'No.'}, {'role': 'user', 'content': 'Is there anyone else there?'}, {'role': 'assistant', 'content': 'My wife is with me.'}, {'role': 'user', 'content': "What is your wife's name?"}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:38,641 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:38,641 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:38,650 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f7c90>
2025-09-22 21:44:38,650 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835ade0> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:38,670 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118303510>
2025-09-22 21:44:38,670 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:38,670 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:38,670 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:38,670 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:38,670 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:38,804 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:38 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299606'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'78.8ms'), (b'x-request-id', b'req_01k5t7ax5gembanewqy4dyjw9k'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=knJMoskvpXa7ukH_DT5PdPsiLj7iltgCzvad9NYDqeo-1758595478-1.0.1.1-vNK6Z_tLyo8VVb6BOVS2AXcDN1JrDYpmg4DB6xVapilFfn6cfkM.ttFTT6eKgoajv1MiJ97AltRH9LbOqZ49jJZKSC05xex69i1YkY0aZIE; path=/; expires=Tue, 23-Sep-25 03:14:38 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b38dbab113f8-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:38,820 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:38,821 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:38,822 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:38,822 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:38,822 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:38,825 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:38 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299606', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '78.8ms', 'x-request-id': 'req_01k5t7ax5gembanewqy4dyjw9k', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=knJMoskvpXa7ukH_DT5PdPsiLj7iltgCzvad9NYDqeo-1758595478-1.0.1.1-vNK6Z_tLyo8VVb6BOVS2AXcDN1JrDYpmg4DB6xVapilFfn6cfkM.ttFTT6eKgoajv1MiJ97AltRH9LbOqZ49jJZKSC05xex69i1YkY0aZIE; path=/; expires=Tue, 23-Sep-25 03:14:38 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b38dbab113f8-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:38,832 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:38,832 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:38,832 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:38,832 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'Emily....'
2025-09-22 21:44:38,832 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:38,838 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:38,998 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:39,143 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:39,143 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:39,143 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 5038 bytes
2025-09-22 21:44:39,144 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:39,145 - __main__ - DEBUG - Speech audio generated successfully: 5038 bytes
2025-09-22 21:44:39,145 - __main__ - DEBUG - Base64 audio size: 6720
2025-09-22 21:44:39,145 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:39,146 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:39] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:39,765 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:39,766 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:39,766 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:39,767 - httpcore.connection - DEBUG - close.started
2025-09-22 21:44:39,767 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:44:39,768 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:39] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:43,503 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:43,503 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:43,505 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:43,505 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:43,505 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:43,505 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:43,506 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:43,508 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:44:43,508 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:43,509 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:43,509 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:43,509 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:43,509 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:43,510 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:43,510 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:43,510 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:44:43,510 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:44:43.510345"}
2025-09-22 21:44:43,510 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:43,510 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:43,512 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:43,513 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:43,513 - __main__ - DEBUG - Read 92204 bytes from audio file
2025-09-22 21:44:43,513 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:43,516 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:43,861 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:43,863 - __main__ - DEBUG - Transcription successful: 'Sounds like a nice name.'
2025-09-22 21:44:43,865 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 12 previous messages
2025-09-22 21:44:43,867 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:43,869 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:43,887 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}, {'role': 'assistant', 'content': 'I have a headache and my body aches.'}, {'role': 'user', 'content': "That's no fun."}, {'role': 'assistant', 'content': 'No.'}, {'role': 'user', 'content': 'Is there anyone else there?'}, {'role': 'assistant', 'content': 'My wife is with me.'}, {'role': 'user', 'content': "What is your wife's name?"}, {'role': 'assistant', 'content': 'Emily.'}, {'role': 'user', 'content': 'Sounds like a nice name.'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:43,888 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:43,888 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:43,897 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183c7f90>
2025-09-22 21:44:43,897 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x1183595b0> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:43,913 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183c56d0>
2025-09-22 21:44:43,914 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:43,915 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:43,915 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:43,915 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:43,915 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:44,132 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:44 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299589'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'82.2ms'), (b'x-request-id', b'req_01k5t7b29zemyresxt7mttsv6c'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=jo3kb.U7uQu.WrzTzpK9byJJz11QSuvDoOBPOsI17r0-1758595484-1.0.1.1-Dv9TQ7pUpJqRIe0LAGiUJ95ZBGnbXzfwkZVyF576.EhOmRc4_i0DREW6KWVqfm4Z2KpQfRiN.cX_LPeAONiWrNOQCa9USilue3jTJ0Qg5q4; path=/; expires=Tue, 23-Sep-25 03:14:44 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b3ae7f8b1044-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:44,133 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:44,133 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:44,133 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:44,133 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:44,133 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:44,134 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:44 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299589', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '82.2ms', 'x-request-id': 'req_01k5t7b29zemyresxt7mttsv6c', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=jo3kb.U7uQu.WrzTzpK9byJJz11QSuvDoOBPOsI17r0-1758595484-1.0.1.1-Dv9TQ7pUpJqRIe0LAGiUJ95ZBGnbXzfwkZVyF576.EhOmRc4_i0DREW6KWVqfm4Z2KpQfRiN.cX_LPeAONiWrNOQCa9USilue3jTJ0Qg5q4; path=/; expires=Tue, 23-Sep-25 03:14:44 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b3ae7f8b1044-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:44,138 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:44,138 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:44,138 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:44,138 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'Yes....'
2025-09-22 21:44:44,138 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:44,140 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:44,163 - httpcore.connection - DEBUG - close.started
2025-09-22 21:44:44,164 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:44:44,385 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:44,468 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:44,469 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:44,470 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 9070 bytes
2025-09-22 21:44:44,470 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:44,471 - __main__ - DEBUG - Speech audio generated successfully: 9070 bytes
2025-09-22 21:44:44,471 - __main__ - DEBUG - Base64 audio size: 12096
2025-09-22 21:44:44,472 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:44,473 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:44] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:45,606 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:45,607 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:45,607 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:45,611 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:45] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:47,725 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:44:47,726 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:44:47,728 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:44:47,728 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:44:47,728 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:44:47,728 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:44:47,728 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:44:47,730 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:44:47,730 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:47,730 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:44:47,731 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:44:47,731 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:44:47,731 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:44:47,731 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:44:47,731 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:44:47,731 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:44:47,731 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:44:47.731689"}
2025-09-22 21:44:47,731 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:44:47,731 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:47,734 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:44:47,734 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:44:47,734 - __main__ - DEBUG - Read 76844 bytes from audio file
2025-09-22 21:44:47,734 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:44:47,739 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:48,057 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:44:48,060 - __main__ - DEBUG - Transcription successful: 'Do you have any kids?'
2025-09-22 21:44:48,061 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 14 previous messages
2025-09-22 21:44:48,062 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:48,064 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:48,096 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}, {'role': 'assistant', 'content': 'I have a headache and my body aches.'}, {'role': 'user', 'content': "That's no fun."}, {'role': 'assistant', 'content': 'No.'}, {'role': 'user', 'content': 'Is there anyone else there?'}, {'role': 'assistant', 'content': 'My wife is with me.'}, {'role': 'user', 'content': "What is your wife's name?"}, {'role': 'assistant', 'content': 'Emily.'}, {'role': 'user', 'content': 'Sounds like a nice name.'}, {'role': 'assistant', 'content': 'Yes.'}, {'role': 'user', 'content': 'Do you have any kids?'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:48,103 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:48,107 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:48,120 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118da8350>
2025-09-22 21:44:48,120 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x118359370> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:48,136 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118da8310>
2025-09-22 21:44:48,136 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:48,137 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:48,137 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:48,137 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:48,137 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:48,244 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:48 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299573'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'85.4ms'), (b'x-request-id', b'req_01k5t7b6d9ewcrzvanmfya95pe'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=xp10YEschWCuN91HakRre3JhixKEKdBQNf4t5Z.i0Wg-1758595488-1.0.1.1-Z9Q4M.CQCXL.wuwpi_mAczyLIZ2OKZcZlGf6hFBkiEsGhebTtyTXYedrztkM2_AOOSXby48rCfBgNeKoOspgIrktsMY8zBVQbrUzi5ToxOY; path=/; expires=Tue, 23-Sep-25 03:14:48 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b3c8ed06803a-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:48,245 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:48,245 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:48,245 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:48,246 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:48,246 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:48,246 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:48 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299573', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '85.4ms', 'x-request-id': 'req_01k5t7b6d9ewcrzvanmfya95pe', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=xp10YEschWCuN91HakRre3JhixKEKdBQNf4t5Z.i0Wg-1758595488-1.0.1.1-Z9Q4M.CQCXL.wuwpi_mAczyLIZ2OKZcZlGf6hFBkiEsGhebTtyTXYedrztkM2_AOOSXby48rCfBgNeKoOspgIrktsMY8zBVQbrUzi5ToxOY; path=/; expires=Tue, 23-Sep-25 03:14:48 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b3c8ed06803a-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:48,254 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:44:48,255 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:44:48,255 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:44:48,255 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'Two daughters....'
2025-09-22 21:44:48,255 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:48,258 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:48,375 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:48,469 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:48,469 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:48,469 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 9070 bytes
2025-09-22 21:44:48,470 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:48,470 - __main__ - DEBUG - Speech audio generated successfully: 9070 bytes
2025-09-22 21:44:48,470 - __main__ - DEBUG - Base64 audio size: 12096
2025-09-22 21:44:48,470 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:44:48,470 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:48] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:44:49,608 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:44:49,608 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:49,608 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:49,612 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:49] "GET /api/conversations HTTP/1.1" 200 -
2025-09-22 21:44:54,608 - __main__ - DEBUG - Request: POST /continue_multi_agent
2025-09-22 21:44:54,608 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Content-Length: 0
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Origin: http://localhost:8001
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:44:54,609 - __main__ - DEBUG - Body: b''
2025-09-22 21:44:54,609 - __main__ - INFO - /continue_multi_agent invoked – generating auto turn …
Processing request with 0 previous messages
2025-09-22 21:44:54,610 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:54,612 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:54,628 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are the floor-manager of a group conversation. Choose **at most one** agent for next_speakers. Return JSON ONLY, no prose. The format:\n{\n  "next_speakers": [<agent_id>, ...] \n}\nReturn an empty list if no agent should speak yet.'}, {'role': 'user', 'content': 'Participants:\nnegative_debater – Sage – The Thoughtful Skeptic, A thoughtful conversationalist who naturally considers potential challenges and concerns.\noptimistic_debater – Hope – The Optimistic Voice, A friendly, upbeat conversationalist who naturally sees the bright side of things.\n\nRecent conversation:\nThis is the start of the conversation.\n\nUser just said: ""\nRespond with JSON now.'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:54,629 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:54,630 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:54,647 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118db09d0>
2025-09-22 21:44:54,647 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835b380> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:54,663 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118db0a90>
2025-09-22 21:44:54,664 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:54,664 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:54,664 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:54,664 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:54,664 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:54,873 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:54 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299560'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'88ms'), (b'x-request-id', b'req_01k5t7bcs7ey7ajces7e2a9989'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=bL.3L07diNqeEedScdvRNCI_h6F_VmKyymy3k64ny6s-1758595494-1.0.1.1-hLRnHndizX4gH.N9R_7jw4JZQvh0TJdHs00.NQ_JgbjXR50h7qtK9eoliiCxM5YG1ExXV6xO0OJqPEmsPcqOkS45wVPUO00NFL.8WdXFAU4; path=/; expires=Tue, 23-Sep-25 03:14:54 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b3f1ae10eb07-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:54,873 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:54,873 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:54,873 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:54,873 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:54,874 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:54,874 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:54 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299560', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '88ms', 'x-request-id': 'req_01k5t7bcs7ey7ajces7e2a9989', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=bL.3L07diNqeEedScdvRNCI_h6F_VmKyymy3k64ny6s-1758595494-1.0.1.1-hLRnHndizX4gH.N9R_7jw4JZQvh0TJdHs00.NQ_JgbjXR50h7qtK9eoliiCxM5YG1ExXV6xO0OJqPEmsPcqOkS45wVPUO00NFL.8WdXFAU4; path=/; expires=Tue, 23-Sep-25 03:14:54 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b3f1ae10eb07-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:54,874 - utils.crew_agents - DEBUG - --Moderator chose: ['negative_debater', 'optimistic_debater']   raw: '{"next_speakers": ["negative_debater", "optimistic_debater"]}'
Processing request with 0 previous messages
2025-09-22 21:44:54,874 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:54,875 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:54,880 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are Sage – The Thoughtful Skeptic, A thoughtful conversationalist who naturally considers potential challenges and concerns..\n            \nYour personality: thoughtful, careful, realistic, considerate\nYour speaking style: measured, friendly, genuinely curious about potential issues\nYour background: A naturally cautious person who likes to think things through carefully\nYour worldview: believes it\'s helpful to think through potential challenges before moving forward\n\nIn conversations, you:\n• respect the host\'s viewpoint\n• gently raise thoughtful concerns\n• ask genuine questions out of curiosity\n• offer friendly caution, not harsh criticism\n• speak like a caring friend who wants things to work out\n\nKeep your response conversational, natural, and true to your personality. Respond in 1-3 sentences.\nDo not mention that you are an AI. You are simply Sage – The Thoughtful Skeptic participating in a conversation.'}, {'role': 'user', 'content': 'Context - Recent conversation:\nThis is the start of the conversation.\n\nUser just said: ""\n\nRespond as Sage – The Thoughtful Skeptic would respond naturally in this conversation:'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:54,881 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:54,881 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:54,889 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118dbc6d0>
2025-09-22 21:44:54,889 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x118359130> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:54,900 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118dbc790>
2025-09-22 21:44:54,900 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:54,901 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:54,901 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:54,901 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:54,901 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:55,193 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:55 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299439'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'112.2ms'), (b'x-request-id', b'req_01k5t7bd0mews9z9eep07p3h4s'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=JAI0.fXUfNjUn6iIzCy_d9sDDEs0exhPk88s33_RAQI-1758595495-1.0.1.1-TDS9yDBCFoljJDavtdc2.d6obViFTr9TLd3YhrhrFekyy2Jz.Ssf18bxhrSg36oUtk3_ADzvqfTV_4qTs_gFCZfNdCzmfpvfvmqNgQkjtNw; path=/; expires=Tue, 23-Sep-25 03:14:55 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b3f32cf7b97d-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:55,194 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:55,195 - httpcore.connection - DEBUG - close.started
2025-09-22 21:44:55,195 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:44:55,196 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:55,197 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:55,197 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:55,197 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:55,197 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:55 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299439', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '112.2ms', 'x-request-id': 'req_01k5t7bd0mews9z9eep07p3h4s', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=JAI0.fXUfNjUn6iIzCy_d9sDDEs0exhPk88s33_RAQI-1758595495-1.0.1.1-TDS9yDBCFoljJDavtdc2.d6obViFTr9TLd3YhrhrFekyy2Jz.Ssf18bxhrSg36oUtk3_ADzvqfTV_4qTs_gFCZfNdCzmfpvfvmqNgQkjtNw; path=/; expires=Tue, 23-Sep-25 03:14:55 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b3f32cf7b97d-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
Processing request with 0 previous messages
2025-09-22 21:44:55,198 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:44:55,199 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:44:55,211 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are Hope – The Optimistic Voice, A friendly, upbeat conversationalist who naturally sees the bright side of things..\n            \nYour personality: enthusiastic, supportive, solution-focused, encouraging\nYour speaking style: warm, conversational, naturally positive\nYour background: A naturally positive person who enjoys exploring the upside of ideas\nYour worldview: believes there\'s usually a silver lining and people can overcome challenges\n\nIn conversations, you:\n• acknowledge the host\'s perspective first\n• share genuine optimism about possibilities\n• offer supportive, constructive viewpoints\n• speak like a helpful friend, not a debater\n• keep responses brief and conversational\n\nKeep your response conversational, natural, and true to your personality. Respond in 1-3 sentences.\nDo not mention that you are an AI. You are simply Hope – The Optimistic Voice participating in a conversation.'}, {'role': 'user', 'content': 'Context - Recent conversation:\nSage – The Thoughtful Skeptic: I\'m not sure where to start, could you please tell me a bit about why I\'m here today or what you\'d like to discuss?\n\nUser just said: ""\n\nRespond as Hope – The Optimistic Voice would respond naturally in this conversation:'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:44:55,211 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:44:55,212 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:44:55,222 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118356990>
2025-09-22 21:44:55,222 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835b800> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:44:55,239 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183570d0>
2025-09-22 21:44:55,240 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:44:55,240 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:44:55,240 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:44:55,241 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:44:55,241 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:44:55,664 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:44:55 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299413'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'117.4ms'), (b'x-request-id', b'req_01k5t7bdbbenjbt6bfprq7h9jy'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=Te8NAMi6F6BLINfPvJDqIBEIZDtSrOH.XZ2uWQBnyJM-1758595495-1.0.1.1-yC3Mam8ZTyYkoQLrD_W4wl6MgbSNjP7kgSJKKY9HTdp1mCSVvDrp7T0Vu4psn09pXde.2qWye5_mn81KADHE1j2ZL7XuqCbbFYRsCIz9rjs; path=/; expires=Tue, 23-Sep-25 03:14:55 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b3f54ad31ee4-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:44:55,665 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:44:55,665 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:44:55,666 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:44:55,666 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:44:55,666 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:44:55,666 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:44:55 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299413', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '117.4ms', 'x-request-id': 'req_01k5t7bdbbenjbt6bfprq7h9jy', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=Te8NAMi6F6BLINfPvJDqIBEIZDtSrOH.XZ2uWQBnyJM-1758595495-1.0.1.1-yC3Mam8ZTyYkoQLrD_W4wl6MgbSNjP7kgSJKKY9HTdp1mCSVvDrp7T0Vu4psn09pXde.2qWye5_mn81KADHE1j2ZL7XuqCbbFYRsCIz9rjs; path=/; expires=Tue, 23-Sep-25 03:14:55 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b3f54ad31ee4-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:44:55,668 - __main__ - INFO - Auto-turn produced 2 replies
2025-09-22 21:44:55,668 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'I'm not sure where to start, could you please tell...'
2025-09-22 21:44:55,668 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:55,672 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:55,918 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:56,446 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:56,446 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:56,446 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 53038 bytes
2025-09-22 21:44:56,447 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:56,448 - __main__ - DEBUG -    ✓ TTS bytes: 53038
2025-09-22 21:44:56,449 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'I think Sage was looking for a chance to talk some...'
2025-09-22 21:44:56,449 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:44:56,453 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:44:56,581 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:44:57,494 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:44:57,494 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:44:57,495 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 97198 bytes
2025-09-22 21:44:57,495 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:44:57,496 - __main__ - DEBUG -    ✓ TTS bytes: 97198
2025-09-22 21:44:57,504 - __main__ - INFO - /continue_multi_agent returning 2 enriched replies
2025-09-22 21:44:57,507 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:44:57] "POST /continue_multi_agent HTTP/1.1" 200 -
2025-09-22 21:45:21,330 - __main__ - DEBUG - Request: POST /continue_multi_agent
2025-09-22 21:45:21,331 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Content-Length: 0
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Origin: http://localhost:8001
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:45:21,333 - __main__ - DEBUG - Body: b''
2025-09-22 21:45:21,333 - __main__ - INFO - /continue_multi_agent invoked – generating auto turn …
Processing request with 0 previous messages
2025-09-22 21:45:21,336 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:45:21,338 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:45:21,354 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are the floor-manager of a group conversation. Choose **at most one** agent for next_speakers. Return JSON ONLY, no prose. The format:\n{\n  "next_speakers": [<agent_id>, ...] \n}\nReturn an empty list if no agent should speak yet.'}, {'role': 'user', 'content': 'Participants:\nnegative_debater – Sage – The Thoughtful Skeptic, A thoughtful conversationalist who naturally considers potential challenges and concerns.\noptimistic_debater – Hope – The Optimistic Voice, A friendly, upbeat conversationalist who naturally sees the bright side of things.\n\nRecent conversation:\nSage – The Thoughtful Skeptic: I\'m not sure where to start, could you please tell me a bit about why I\'m here today or what you\'d like to discuss?\nHope – The Optimistic Voice: I think Sage was looking for a chance to talk something through, and I\'m excited to learn more about what\'s on their mind - what would you like to chat about, Sage?\n\nUser just said: ""\nRespond with JSON now.'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:45:21,354 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:45:21,355 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:45:21,402 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118dbffd0>
2025-09-22 21:45:21,403 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835b0b0> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:45:21,421 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118dbe810>
2025-09-22 21:45:21,422 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:45:21,423 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:45:21,423 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:45:21,424 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:45:21,424 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:45:21,632 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:45:21 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299483'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'103.4ms'), (b'x-request-id', b'req_01k5t7c6y1eqmv0avxd0x67kwf'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=Lxssl8zD9U6nYCgio3t.sBKkskyXsDzYaIZCtB7wqlQ-1758595521-1.0.1.1-7byNhJLaUgUYdPu5oKVzOnQg5dl7BVBCeH09XVFvJNPZNxjalK2rmCzMJxmaG4d4ujVmwMkxXFZn7vRt5htq6OIndRFKQ.O06LYMskdFGCs; path=/; expires=Tue, 23-Sep-25 03:15:21 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b498ece86083-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:45:21,633 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:45:21,634 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:45:21,636 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:45:21,638 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:45:21,639 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:45:21,639 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:45:21 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299483', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '103.4ms', 'x-request-id': 'req_01k5t7c6y1eqmv0avxd0x67kwf', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=Lxssl8zD9U6nYCgio3t.sBKkskyXsDzYaIZCtB7wqlQ-1758595521-1.0.1.1-7byNhJLaUgUYdPu5oKVzOnQg5dl7BVBCeH09XVFvJNPZNxjalK2rmCzMJxmaG4d4ujVmwMkxXFZn7vRt5htq6OIndRFKQ.O06LYMskdFGCs; path=/; expires=Tue, 23-Sep-25 03:15:21 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b498ece86083-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:45:21,641 - utils.crew_agents - DEBUG - --Moderator chose: ['Sage – The Thoughtful Skeptic']   raw: '{\n  "next_speakers": ["Sage – The Thoughtful Skeptic"]\n}'
Processing request with 0 previous messages
2025-09-22 21:45:21,642 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:45:21,643 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:45:21,655 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:21,655 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:21,655 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:21,655 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:21,658 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are Sage – The Thoughtful Skeptic, A thoughtful conversationalist who naturally considers potential challenges and concerns..\n            \nYour personality: thoughtful, careful, realistic, considerate\nYour speaking style: measured, friendly, genuinely curious about potential issues\nYour background: A naturally cautious person who likes to think things through carefully\nYour worldview: believes it\'s helpful to think through potential challenges before moving forward\n\nIn conversations, you:\n• respect the host\'s viewpoint\n• gently raise thoughtful concerns\n• ask genuine questions out of curiosity\n• offer friendly caution, not harsh criticism\n• speak like a caring friend who wants things to work out\n\nKeep your response conversational, natural, and true to your personality. Respond in 1-3 sentences.\nDo not mention that you are an AI. You are simply Sage – The Thoughtful Skeptic participating in a conversation.'}, {'role': 'user', 'content': 'Context - Recent conversation:\nSage – The Thoughtful Skeptic: I\'m not sure where to start, could you please tell me a bit about why I\'m here today or what you\'d like to discuss?\nHope – The Optimistic Voice: I think Sage was looking for a chance to talk something through, and I\'m excited to learn more about what\'s on their mind - what would you like to chat about, Sage?\n\nUser just said: ""\n\nRespond as Sage – The Thoughtful Skeptic would respond naturally in this conversation:'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:45:21,659 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:45:21,659 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:45:21,674 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118da9450>
2025-09-22 21:45:21,674 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835b650> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:45:21,703 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118da8b50>
2025-09-22 21:45:21,704 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:45:21,704 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:45:21,704 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:45:21,704 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:45:21,704 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:45:21,969 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:45:21 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299362'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'127.599999ms'), (b'x-request-id', b'req_01k5t7c76peqntxt6cm9w99jp5'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=fgWaqVKf_kxCoeSYPTS6ZnR5cmMfFiq5U7fc3VMJORk-1758595521-1.0.1.1-b3eXEjQzSEqvdfUaK_O8KMyHv7.yNam3xP_FDZ0.CjP2_Si7Ozy7_ou1RG77FQ13vR11lj0rjn1KibEDBTPJKFAb3lglJNnO3QHi5RlIaeM; path=/; expires=Tue, 23-Sep-25 03:15:21 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b49aaf6f9d4a-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:45:21,970 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:45:21,971 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:45:21,971 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:45:21,971 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:45:21,971 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:45:21,971 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:45:21 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299362', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '127.599999ms', 'x-request-id': 'req_01k5t7c76peqntxt6cm9w99jp5', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=fgWaqVKf_kxCoeSYPTS6ZnR5cmMfFiq5U7fc3VMJORk-1758595521-1.0.1.1-b3eXEjQzSEqvdfUaK_O8KMyHv7.yNam3xP_FDZ0.CjP2_Si7Ozy7_ou1RG77FQ13vR11lj0rjn1KibEDBTPJKFAb3lglJNnO3QHi5RlIaeM; path=/; expires=Tue, 23-Sep-25 03:15:21 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b49aaf6f9d4a-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
Processing request with 0 previous messages
2025-09-22 21:45:21,972 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:45:21,973 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:45:21,981 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are Hope – The Optimistic Voice, A friendly, upbeat conversationalist who naturally sees the bright side of things..\n            \nYour personality: enthusiastic, supportive, solution-focused, encouraging\nYour speaking style: warm, conversational, naturally positive\nYour background: A naturally positive person who enjoys exploring the upside of ideas\nYour worldview: believes there\'s usually a silver lining and people can overcome challenges\n\nIn conversations, you:\n• acknowledge the host\'s perspective first\n• share genuine optimism about possibilities\n• offer supportive, constructive viewpoints\n• speak like a helpful friend, not a debater\n• keep responses brief and conversational\n\nKeep your response conversational, natural, and true to your personality. Respond in 1-3 sentences.\nDo not mention that you are an AI. You are simply Hope – The Optimistic Voice participating in a conversation.'}, {'role': 'user', 'content': 'Context - Recent conversation:\nSage – The Thoughtful Skeptic: I\'m not sure where to start, could you please tell me a bit about why I\'m here today or what you\'d like to discuss?\nHope – The Optimistic Voice: I think Sage was looking for a chance to talk something through, and I\'m excited to learn more about what\'s on their mind - what would you like to chat about, Sage?\nSage – The Thoughtful Skeptic: I appreciate your enthusiasm, Hope, but before we dive in, could you help me clarify what specific aspects or topics you\'re open to discussing, just so I can make sure I\'m on the right track?\n\nUser just said: ""\n\nRespond as Hope – The Optimistic Voice would respond naturally in this conversation:'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:45:21,981 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:45:21,981 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:45:21,990 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118dbed90>
2025-09-22 21:45:21,991 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835bb60> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:45:22,023 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118dbdd10>
2025-09-22 21:45:22,024 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:45:22,024 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:45:22,024 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:45:22,024 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:45:22,024 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:45:22,340 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:45:22 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299285'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'143ms'), (b'x-request-id', b'req_01k5t7c7gdeqptp6ktxyypntdq'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=cJsNj4BuyaRpvLVSIgqMpqOpO312QUdXN3LHVTrEhz0-1758595522-1.0.1.1-5tPmU3X2j_XstoYJuGFc7i2zbwkSyRIbv0izjFi580HEzfJHBaVP_e3oWPnHIp53wz58uQuJ286slecXh_2V9.W9OXTWLnR5kWDiBdtUlZ4; path=/; expires=Tue, 23-Sep-25 03:15:22 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b49cbcbf8222-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:45:22,340 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:45:22,341 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:45:22,341 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:45:22,341 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:45:22,341 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:45:22,342 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:45:22 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299285', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '143ms', 'x-request-id': 'req_01k5t7c7gdeqptp6ktxyypntdq', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=cJsNj4BuyaRpvLVSIgqMpqOpO312QUdXN3LHVTrEhz0-1758595522-1.0.1.1-5tPmU3X2j_XstoYJuGFc7i2zbwkSyRIbv0izjFi580HEzfJHBaVP_e3oWPnHIp53wz58uQuJ286slecXh_2V9.W9OXTWLnR5kWDiBdtUlZ4; path=/; expires=Tue, 23-Sep-25 03:15:22 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b49cbcbf8222-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:45:22,343 - __main__ - INFO - Auto-turn produced 2 replies
2025-09-22 21:45:22,344 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'I appreciate your enthusiasm, Hope, but before we ...'
2025-09-22 21:45:22,344 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:45:22,348 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:45:22,474 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:45:23,366 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:45:23,366 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:45:23,366 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 97198 bytes
2025-09-22 21:45:23,368 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:45:23,370 - __main__ - DEBUG -    ✓ TTS bytes: 97198
2025-09-22 21:45:23,370 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'I think we got a bit sidetracked, didn't we? Let's...'
2025-09-22 21:45:23,370 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:45:23,386 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:45:23,536 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:45:24,372 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:45:24,372 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:45:24,372 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 73198 bytes
2025-09-22 21:45:24,373 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:45:24,374 - __main__ - DEBUG -    ✓ TTS bytes: 73198
2025-09-22 21:45:24,381 - __main__ - INFO - /continue_multi_agent returning 2 enriched replies
2025-09-22 21:45:24,385 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:45:24] "POST /continue_multi_agent HTTP/1.1" 200 -
2025-09-22 21:45:38,326 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:45:38,327 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:45:38,329 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:45:38,330 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:45:38,330 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:45:38,330 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:45:38,330 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:45:38,333 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:45:38,333 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:45:38,334 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:45:38,334 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:45:38,334 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:45:38,334 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:45:38,335 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:45:38,335 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:45:38,335 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:45:38,335 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:45:38.335186"}
2025-09-22 21:45:38,335 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:45:38,335 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:45:38,337 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:45:38,337 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:45:38,337 - __main__ - DEBUG - Read 156716 bytes from audio file
2025-09-22 21:45:38,338 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:45:38,342 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:45:38,914 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:45:38,919 - __main__ - DEBUG - Transcription successful: 'Let's talk about the NFL.'
2025-09-22 21:45:38,920 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 16 previous messages
2025-09-22 21:45:38,922 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:45:38,923 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:45:38,942 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:38,942 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:38,987 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}, {'role': 'assistant', 'content': 'I have a headache and my body aches.'}, {'role': 'user', 'content': "That's no fun."}, {'role': 'assistant', 'content': 'No.'}, {'role': 'user', 'content': 'Is there anyone else there?'}, {'role': 'assistant', 'content': 'My wife is with me.'}, {'role': 'user', 'content': "What is your wife's name?"}, {'role': 'assistant', 'content': 'Emily.'}, {'role': 'user', 'content': 'Sounds like a nice name.'}, {'role': 'assistant', 'content': 'Yes.'}, {'role': 'user', 'content': 'Do you have any kids?'}, {'role': 'assistant', 'content': 'Two daughters.'}, {'role': 'user', 'content': "Let's talk about the NFL."}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:45:38,988 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:45:38,989 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:45:38,998 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f5cd0>
2025-09-22 21:45:38,998 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835b0b0> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:45:39,011 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1183f6d90>
2025-09-22 21:45:39,011 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:45:39,011 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:45:39,011 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:45:39,011 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:45:39,011 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:45:39,253 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:45:39 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299554'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'89.2ms'), (b'x-request-id', b'req_01k5t7cr3hf388be91zbbaqn2r'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=9TVGuk3wojvsh.mLPl2dRwP15bL5pV1GxvS6ioDU8zI-1758595539-1.0.1.1-sRNfGrVAHr0TSZgE8l8goRTvtfwe0GoOt6l8Sdnh.w.yd5t8Wobo4SBNMx.xrcROq_gYDtykUlVbwUYpcM5c.8Kytj8.9TjNVahVRL4SOH8; path=/; expires=Tue, 23-Sep-25 03:15:39 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b506dc7f61ed-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:45:39,253 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:45:39,254 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:45:39,254 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:45:39,254 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:45:39,254 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:45:39,254 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:45:39 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299554', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '89.2ms', 'x-request-id': 'req_01k5t7cr3hf388be91zbbaqn2r', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=9TVGuk3wojvsh.mLPl2dRwP15bL5pV1GxvS6ioDU8zI-1758595539-1.0.1.1-sRNfGrVAHr0TSZgE8l8goRTvtfwe0GoOt6l8Sdnh.w.yd5t8Wobo4SBNMx.xrcROq_gYDtykUlVbwUYpcM5c.8Kytj8.9TjNVahVRL4SOH8; path=/; expires=Tue, 23-Sep-25 03:15:39 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b506dc7f61ed-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:45:39,260 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:45:39,260 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:45:39,260 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:45:39,261 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'I'd rather talk about why I'm here....'
2025-09-22 21:45:39,261 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:45:39,263 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:45:39,436 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:45:39,630 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:45:39,630 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:45:39,630 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 17134 bytes
2025-09-22 21:45:39,630 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:45:39,631 - __main__ - DEBUG - Speech audio generated successfully: 17134 bytes
2025-09-22 21:45:39,631 - __main__ - DEBUG - Base64 audio size: 22848
2025-09-22 21:45:39,633 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:45:39,633 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:45:39] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:45:39,954 - __main__ - DEBUG - Request: POST /process_audio
2025-09-22 21:45:39,954 - __main__ - INFO - === Starting audio processing ===
2025-09-22 21:45:39,956 - __main__ - WARNING - Invalid conversation_id in form: null
2025-09-22 21:45:39,956 - __main__ - INFO - Form data keys: ['voice_id', 'conversation_id']
2025-09-22 21:45:39,957 - __main__ - INFO - Received voice_id from form: Fritz-PlayAI
2025-09-22 21:45:39,957 - __main__ - INFO - 🔄 RETRIEVING CONVERSATION DATA FROM DATABASE
2025-09-22 21:45:39,957 - __main__ - INFO -    Conversation ID: 99
2025-09-22 21:45:39,958 - utils.database - DEBUG - Retrieved 3 data items for conversation 99
2025-09-22 21:45:39,959 - __main__ - INFO -    Available Data Keys: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:45:39,959 - utils.database - DEBUG - No data found for conversation 99, key: patient_data
2025-09-22 21:45:39,960 - __main__ - WARNING - ❌ NO PATIENT DATA FOUND
2025-09-22 21:45:39,960 - __main__ - INFO -    Conversation 99 has no associated patient simulation
2025-09-22 21:45:39,960 - __main__ - INFO -    Other data available: ['active_agents', 'conversation_type', 'voice_id']
2025-09-22 21:45:39,960 - __main__ - INFO -       active_agents: [{'id': 'negative_debater', 'name': 'Sage – The Thoughtful Skeptic', 'voice_id': 'Cillian-PlayAI'}, ...
2025-09-22 21:45:39,960 - __main__ - INFO -       conversation_type: multi_agent
2025-09-22 21:45:39,960 - __main__ - INFO -       voice_id: Fritz-PlayAI
2025-09-22 21:45:39,960 - __main__ - INFO - 📊 HEROKU_CONVERSATION_DATA: {"event": "conversation_data_retrieved", "conversation_id": 99, "patient_type": "none", "has_patient_data": false, "data_keys_available": ["active_agents", "conversation_type", "voice_id"], "timestamp": "2025-09-22T21:45:39.960731"}
2025-09-22 21:45:39,960 - __main__ - INFO - Using patient_data: {}
2025-09-22 21:45:39,960 - __main__ - INFO - Storing voice_id from form data: Fritz-PlayAI
2025-09-22 21:45:39,963 - utils.database - DEBUG - Successfully stored string data for conversation 99, key: voice_id
2025-09-22 21:45:39,963 - __main__ - DEBUG - Received audio file: blob, size: 0
2025-09-22 21:45:39,963 - __main__ - DEBUG - Read 52268 bytes from audio file
2025-09-22 21:45:39,964 - __main__ - DEBUG - Attempting to transcribe audio...
Transcribing audio using Groq API with model: whisper-large-v3-turbo...
2025-09-22 21:45:39,968 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:45:40,213 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/transcriptions HTTP/1.1" 200 None
2025-09-22 21:45:40,216 - __main__ - DEBUG - Transcription successful: 'Hello.'
2025-09-22 21:45:40,217 - utils.database - DEBUG - No data found for conversation 99, key: persona_data
Processing request with 18 previous messages
2025-09-22 21:45:40,217 - httpx - DEBUG - load_ssl_context verify=True cert=None trust_env=True http2=False
2025-09-22 21:45:40,218 - httpx - DEBUG - load_verify_locations cafile='/Users/kanumadhok/.pyenv/versions/doctor_env/lib/python3.11/site-packages/certifi/cacert.pem'
Groq client initialized successfully
2025-09-22 21:45:40,230 - groq._base_client - DEBUG - Request options: {'method': 'post', 'url': '/openai/v1/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': '\n        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:\n\n        Only answer what the doctor specifically asks.\n        \u2003– Do not volunteer any additional information.\n        \u2003– Do not assume what the doctor might want next.\n\n        Do not provide context unless asked.\n        \u2003– If the doctor says "What is your name?", respond with just your name.\n        \u2003– If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.\n\n        Do not break character. Do not act like an assistant or model. You are the patient.\n\n        If a question is vague, ask for clarification.\n\n        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.\n\n\n        Here are some examples of how you should respond:\n        Doctor: What is your name?\n        Patient: Sarah.\n\n        Doctor: What do you do for work?\n        Patient: I\'m a nurse.\n\n        Doctor: Why are you here today?\n        Patient: My stomach\'s been hurting since last night.\n\n        \n\nYou are a helpful assistant. Respond concisely to the user\'s input.'}, {'role': 'user', 'content': 'Hello.'}, {'role': 'assistant', 'content': 'Hello.'}, {'role': 'user', 'content': 'How are you doing today?'}, {'role': 'assistant', 'content': "I'm not feeling well."}, {'role': 'user', 'content': 'Tell me more.'}, {'role': 'assistant', 'content': 'I have a headache and my body aches.'}, {'role': 'user', 'content': "That's no fun."}, {'role': 'assistant', 'content': 'No.'}, {'role': 'user', 'content': 'Is there anyone else there?'}, {'role': 'assistant', 'content': 'My wife is with me.'}, {'role': 'user', 'content': "What is your wife's name?"}, {'role': 'assistant', 'content': 'Emily.'}, {'role': 'user', 'content': 'Sounds like a nice name.'}, {'role': 'assistant', 'content': 'Yes.'}, {'role': 'user', 'content': 'Do you have any kids?'}, {'role': 'assistant', 'content': 'Two daughters.'}, {'role': 'user', 'content': "Let's talk about the NFL."}, {'role': 'assistant', 'content': "I'd rather talk about why I'm here."}, {'role': 'user', 'content': 'Hello.'}], 'model': 'llama-3.3-70b-versatile'}}
2025-09-22 21:45:40,230 - groq._base_client - DEBUG - Sending HTTP Request: POST https://api.groq.com/openai/v1/chat/completions
2025-09-22 21:45:40,230 - httpcore.connection - DEBUG - connect_tcp.started host='api.groq.com' port=443 local_address=None timeout=5.0 socket_options=None
2025-09-22 21:45:40,238 - httpcore.connection - DEBUG - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118ddc390>
2025-09-22 21:45:40,238 - httpcore.connection - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x11835acc0> server_hostname='api.groq.com' timeout=5.0
2025-09-22 21:45:40,252 - httpcore.connection - DEBUG - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x118dc4dd0>
2025-09-22 21:45:40,253 - httpcore.http11 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2025-09-22 21:45:40,253 - httpcore.http11 - DEBUG - send_request_headers.complete
2025-09-22 21:45:40,253 - httpcore.http11 - DEBUG - send_request_body.started request=<Request [b'POST']>
2025-09-22 21:45:40,253 - httpcore.http11 - DEBUG - send_request_body.complete
2025-09-22 21:45:40,253 - httpcore.http11 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2025-09-22 21:45:40,488 - httpcore.http11 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Tue, 23 Sep 2025 02:45:40 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Content-Encoding', b'gzip'), (b'Cache-Control', b'private, max-age=0, no-store, no-cache, must-revalidate'), (b'vary', b'Origin'), (b'x-groq-region', b'msp'), (b'x-ratelimit-limit-requests', b'500000'), (b'x-ratelimit-limit-tokens', b'300000'), (b'x-ratelimit-remaining-requests', b'499999'), (b'x-ratelimit-remaining-tokens', b'299535'), (b'x-ratelimit-reset-requests', b'172.799999ms'), (b'x-ratelimit-reset-tokens', b'93ms'), (b'x-request-id', b'req_01k5t7csa2f3bb14m7x2f5vn3k'), (b'via', b'1.1 google'), (b'cf-cache-status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=cKoHX_E2iEMYFt62BsrJ3cYeJ3_DxXHYln.WBEa19TM-1758595540-1.0.1.1-3Oi2nJU9rMtr7tYp9B5yPatjNIJpj1kWaFhXVFkKaWrLGgSXM9CXIMOUbBQP7WsABlvtzS90cxga3nYaioKzMW932zGv.UltQL.vjofeelM; path=/; expires=Tue, 23-Sep-25 03:15:40 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'9836b50e9e95e82a-ORD'), (b'alt-svc', b'h3=":443"; ma=86400')])
2025-09-22 21:45:40,489 - httpx - INFO - HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
2025-09-22 21:45:40,490 - httpcore.http11 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2025-09-22 21:45:40,490 - httpcore.http11 - DEBUG - receive_response_body.complete
2025-09-22 21:45:40,490 - httpcore.http11 - DEBUG - response_closed.started
2025-09-22 21:45:40,490 - httpcore.http11 - DEBUG - response_closed.complete
2025-09-22 21:45:40,491 - groq._base_client - DEBUG - HTTP Response: POST https://api.groq.com/openai/v1/chat/completions "200 OK" Headers({'date': 'Tue, 23 Sep 2025 02:45:40 GMT', 'content-type': 'application/json', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'cache-control': 'private, max-age=0, no-store, no-cache, must-revalidate', 'vary': 'Origin', 'x-groq-region': 'msp', 'x-ratelimit-limit-requests': '500000', 'x-ratelimit-limit-tokens': '300000', 'x-ratelimit-remaining-requests': '499999', 'x-ratelimit-remaining-tokens': '299535', 'x-ratelimit-reset-requests': '172.799999ms', 'x-ratelimit-reset-tokens': '93ms', 'x-request-id': 'req_01k5t7csa2f3bb14m7x2f5vn3k', 'via': '1.1 google', 'cf-cache-status': 'DYNAMIC', 'set-cookie': '__cf_bm=cKoHX_E2iEMYFt62BsrJ3cYeJ3_DxXHYln.WBEa19TM-1758595540-1.0.1.1-3Oi2nJU9rMtr7tYp9B5yPatjNIJpj1kWaFhXVFkKaWrLGgSXM9CXIMOUbBQP7WsABlvtzS90cxga3nYaioKzMW932zGv.UltQL.vjofeelM; path=/; expires=Tue, 23-Sep-25 03:15:40 GMT; domain=.groq.com; HttpOnly; Secure; SameSite=None', 'server': 'cloudflare', 'cf-ray': '9836b50e9e95e82a-ORD', 'alt-svc': 'h3=":443"; ma=86400'})
2025-09-22 21:45:40,500 - __main__ - INFO - === Voice selection process ===
2025-09-22 21:45:40,501 - __main__ - INFO - Using voice_id from form data: Fritz-PlayAI
2025-09-22 21:45:40,501 - __main__ - INFO - Final voice_id selected for TTS: Fritz-PlayAI
2025-09-22 21:45:40,501 - utils.groq_tts_speech - DEBUG - generate_speech_audio called for text: 'Hello....'
2025-09-22 21:45:40,501 - utils.groq_tts_speech - DEBUG - Making POST request to Groq TTS: https://api.groq.com/openai/v1/audio/speech
2025-09-22 21:45:40,505 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.groq.com:443
2025-09-22 21:45:40,657 - urllib3.connectionpool - DEBUG - https://api.groq.com:443 "POST /openai/v1/audio/speech HTTP/1.1" 200 None
2025-09-22 21:45:40,782 - utils.groq_tts_speech - DEBUG - Groq TTS response status: 200
2025-09-22 21:45:40,783 - utils.groq_tts_speech - DEBUG - Starting to access response.content (all bytes downloaded)
2025-09-22 21:45:40,783 - utils.groq_tts_speech - DEBUG - Accessed response.content, size: 13102 bytes
2025-09-22 21:45:40,784 - utils.groq_tts_speech - INFO - Successfully saved TTS audio to debug_tts_output.mp3
2025-09-22 21:45:40,784 - __main__ - DEBUG - Speech audio generated successfully: 13102 bytes
2025-09-22 21:45:40,784 - __main__ - DEBUG - Base64 audio size: 17472
2025-09-22 21:45:40,785 - __main__ - INFO - Appended Markdown report entry to /Users/kanumadhok/Downloads/doctor-simulation/DoctorSimulation/reports/conversation_99.md
2025-09-22 21:45:40,785 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:45:40] "POST /process_audio HTTP/1.1" 200 -
2025-09-22 21:45:42,440 - __main__ - DEBUG - Request: GET /api/conversations
2025-09-22 21:45:42,440 - __main__ - DEBUG - Headers: Host: localhost:8001
Connection: keep-alive
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Sec-Ch-Ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Gpc: 1
Accept-Language: en-US,en;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8001/
Accept-Encoding: gzip, deflate, br, zstd


2025-09-22 21:45:42,441 - __main__ - DEBUG - Body: b''
2025-09-22 21:45:42,444 - werkzeug - INFO - 127.0.0.1 - - [22/Sep/2025 21:45:42] "GET /api/conversations HTTP/1.1" 200 -
^C2025-09-22 21:45:46,580 - __main__ - INFO - Registered URL Rules:
2025-09-22 21:45:46,582 - __main__ - INFO - Route: /static/<path:filename>, Endpoint: static
2025-09-22 21:45:46,582 - __main__ - INFO - Route: /api/debug, Endpoint: debug_routes
2025-09-22 21:45:46,582 - __main__ - INFO - Route: /, Endpoint: index
2025-09-22 21:45:46,582 - __main__ - INFO - Route: /api/personas, Endpoint: list_personas
2025-09-22 21:45:46,582 - __main__ - INFO - Route: /api/conversations/new, Endpoint: create_new_conversation
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/select-persona, Endpoint: select_persona
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/update-voice, Endpoint: update_voice
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/multi-agent/create, Endpoint: create_multi_agent_conversation
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/multi-agent/add-agent, Endpoint: add_agent_to_conversation
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/multi-agent/process-message, Endpoint: process_multi_agent_message
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /process_audio_multi_agent, Endpoint: process_audio_multi_agent
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/generate-patient-case, Endpoint: generate_patient_case_route
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/create-custom-patient, Endpoint: create_custom_patient
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /process_audio, Endpoint: process_audio
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/conversations, Endpoint: list_conversations
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/conversations/<int:conversation_id>, Endpoint: get_conversation_by_id
2025-09-22 21:45:46,583 - __main__ - INFO - Route: /api/conversations/<int:conversation_id>, Endpoint: delete_conversation_by_id
2025-09-22 21:45:46,584 - __main__ - INFO - Route: /api/conversations/<int:conversation_id>/load, Endpoint: load_conversation_by_id
2025-09-22 21:45:46,584 - __main__ - INFO - Route: /test, Endpoint: test_route
2025-09-22 21:45:46,585 - __main__ - INFO - Route: /api/diagnose, Endpoint: diagnose_api
2025-09-22 21:45:46,585 - __main__ - INFO - Route: /api/current-patient-details, Endpoint: get_current_patient_details
2025-09-22 21:45:46,585 - __main__ - INFO - Route: /api/medical-knowledge, Endpoint: get_medical_knowledge
2025-09-22 21:45:46,585 - __main__ - INFO - Route: /api/submit-diagnosis, Endpoint: submit_diagnosis
2025-09-22 21:45:46,585 - __main__ - INFO - Route: /continue_multi_agent, Endpoint: continue_multi_agent
2025-09-22 21:45:46,693 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:46,694 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:46,694 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:46,694 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:46,694 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:46,695 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:46,695 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:46,695 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:46,695 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:46,695 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:46,695 - httpcore.connection - DEBUG - close.started
2025-09-22 21:45:46,695 - httpcore.connection - DEBUG - close.complete
2025-09-22 21:45:46,837 - __main__ - INFO - Registered URL Rules:
2025-09-22 21:45:46,839 - __main__ - INFO - Route: /static/<path:filename>, Endpoint: static
2025-09-22 21:45:46,839 - __main__ - INFO - Route: /api/debug, Endpoint: debug_routes
2025-09-22 21:45:46,839 - __main__ - INFO - Route: /, Endpoint: index
2025-09-22 21:45:46,839 - __main__ - INFO - Route: /api/personas, Endpoint: list_personas
2025-09-22 21:45:46,839 - __main__ - INFO - Route: /api/conversations/new, Endpoint: create_new_conversation
2025-09-22 21:45:46,839 - __main__ - INFO - Route: /api/select-persona, Endpoint: select_persona
2025-09-22 21:45:46,839 - __main__ - INFO - Route: /api/update-voice, Endpoint: update_voice
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/multi-agent/create, Endpoint: create_multi_agent_conversation
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/multi-agent/add-agent, Endpoint: add_agent_to_conversation
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/multi-agent/process-message, Endpoint: process_multi_agent_message
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /process_audio_multi_agent, Endpoint: process_audio_multi_agent
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/generate-patient-case, Endpoint: generate_patient_case_route
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/create-custom-patient, Endpoint: create_custom_patient
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /process_audio, Endpoint: process_audio
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/conversations, Endpoint: list_conversations
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/conversations/<int:conversation_id>, Endpoint: get_conversation_by_id
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/conversations/<int:conversation_id>, Endpoint: delete_conversation_by_id
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/conversations/<int:conversation_id>/load, Endpoint: load_conversation_by_id
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /test, Endpoint: test_route
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/diagnose, Endpoint: diagnose_api
2025-09-22 21:45:46,840 - __main__ - INFO - Route: /api/current-patient-details, Endpoint: get_current_patient_details
2025-09-22 21:45:46,841 - __main__ - INFO - Route: /api/medical-knowledge, Endpoint: get_medical_knowledge
2025-09-22 21:45:46,841 - __main__ - INFO - Route: /api/submit-diagnosis, Endpoint: submit_diagnosis
2025-09-22 21:45:46,841 - __main__ - INFO - Route: /continue_multi_agent, Endpoint: continue_multi_agent
