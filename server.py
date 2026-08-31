#!/usr/bin/env python3
"""
Lightweight Web Server for Gemini 3.5 Flash-Lite vs 2.5 Flash 10-K Benchmark.
"""

import http.server
import socketserver
import os
import json
import urllib.parse
from benchmark_10k_ocr import calculate_workload_cost, MODELS_CONFIG

PORT = int(os.environ.get("PORT", 8080))

class BenchmarkHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == "/api/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(MODELS_CONFIG).encode("utf-8"))
            return
            
        elif parsed.path == "/api/calculate":
            query = urllib.parse.parse_qs(parsed.query)
            pages = int(query.get("pages", [100])[0])
            filings = int(query.get("filings", [1000])[0])
            out_tok = int(query.get("out_tokens", [8500])[0])
            cache_hit = float(query.get("cache_hit", [0.60])[0])
            
            res = calculate_workload_cost(pages, filings, out_tok, cache_hit)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return
            
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), BenchmarkHandler) as httpd:
        print(f"[Info] Gemini 10-K OCR Benchmark Server running on http://0.0.0.0:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
