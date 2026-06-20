"""
data/providers/data_gov_tw/oas_adapter_v143.py — OAS/Swagger API metadata adapter v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Parses OAS/Swagger API documentation metadata.
[!] Does not execute unknown code from API specs.
[!] Auth requirement detection — does not bypass authentication.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataGovTwOasAdapter:
    """
    Parses OAS (OpenAPI Specification / Swagger) metadata for data.gov.tw agency APIs.

    Extracts:
    - Endpoint metadata (path, method, description)
    - GET/POST endpoints
    - Query parameters
    - Pagination metadata
    - Auth requirement detection
    - Rate limit hints
    - Response schema
    - API doc URL
    - API version

    Does NOT:
    - Execute code from OAS spec
    - Bypass authentication
    - Auto-call discovered endpoints
    """

    def parse(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Parse an OAS 2.0 (Swagger) or OAS 3.x spec dict."""
        warnings: List[str] = []

        if not isinstance(spec, dict):
            return {
                "success": False,
                "error": "OAS spec is not a dict",
                "endpoints": [],
                "auth_required": False,
                "warnings": [],
            }

        # Detect OAS version
        oas_version = spec.get("openapi") or spec.get("swagger") or "unknown"
        title = (spec.get("info") or {}).get("title", "")
        api_version = (spec.get("info") or {}).get("version", "")
        description = (spec.get("info") or {}).get("description", "")

        # Detect authentication
        auth_required = self._detect_auth(spec)

        # Extract endpoints
        endpoints = self._extract_endpoints(spec, warnings)

        # Extract base URL
        base_url = self._extract_base_url(spec)

        return {
            "success": True,
            "oas_version": str(oas_version),
            "title": title,
            "api_version": api_version,
            "description": description,
            "base_url": base_url,
            "auth_required": auth_required,
            "endpoints": endpoints,
            "endpoint_count": len(endpoints),
            "warnings": warnings,
            "error": None,
        }

    def _detect_auth(self, spec: Dict[str, Any]) -> bool:
        """Detect if any authentication is required."""
        # OAS 3.x
        components = spec.get("components", {})
        if components.get("securitySchemes"):
            return True
        # OAS 2.x
        if spec.get("securityDefinitions"):
            return True
        # Global security
        if spec.get("security"):
            return True
        # Check individual paths
        paths = spec.get("paths", {})
        for _, path_item in paths.items():
            if isinstance(path_item, dict):
                for method in ("get", "post", "put", "delete", "patch"):
                    op = path_item.get(method, {})
                    if isinstance(op, dict) and op.get("security"):
                        return True
        return False

    def _extract_endpoints(
        self, spec: Dict[str, Any], warnings: List[str]
    ) -> List[Dict[str, Any]]:
        paths = spec.get("paths", {})
        endpoints = []
        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method in ("get", "post", "put", "delete", "patch"):
                op = path_item.get(method)
                if not isinstance(op, dict):
                    continue
                params = self._extract_params(op)
                pagination = self._detect_pagination(params, op)
                schema_info = self._extract_response_schema(op)
                endpoints.append({
                    "path": path,
                    "method": method.upper(),
                    "operation_id": op.get("operationId"),
                    "summary": op.get("summary", ""),
                    "description": op.get("description", ""),
                    "parameters": params,
                    "pagination": pagination,
                    "auth_required": bool(op.get("security")),
                    "response_schema": schema_info,
                    "tags": op.get("tags", []),
                })
        return endpoints

    def _extract_params(self, op: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = []
        for p in op.get("parameters", []):
            if isinstance(p, dict):
                result.append({
                    "name": p.get("name"),
                    "in": p.get("in"),
                    "required": p.get("required", False),
                    "type": (p.get("schema") or {}).get("type") or p.get("type"),
                    "description": p.get("description", ""),
                })
        return result

    def _detect_pagination(
        self, params: List[Dict[str, Any]], op: Dict[str, Any]
    ) -> Dict[str, Any]:
        param_names = {p.get("name", "").lower() for p in params}
        paginated = bool(
            param_names & {"page", "offset", "skip", "start", "limit", "size", "pagesize", "pageindex"}
        )
        return {"supported": paginated, "param_names": sorted(param_names & {"page", "offset", "limit", "size"})}

    def _extract_base_url(self, spec: Dict[str, Any]) -> Optional[str]:
        # OAS 3.x
        servers = spec.get("servers", [])
        if servers and isinstance(servers[0], dict):
            return servers[0].get("url")
        # OAS 2.x
        host = spec.get("host")
        if host:
            scheme = (spec.get("schemes") or ["https"])[0]
            base_path = spec.get("basePath", "/")
            return f"{scheme}://{host}{base_path}"
        return None

    def _extract_response_schema(self, op: Dict[str, Any]) -> Dict[str, Any]:
        responses = op.get("responses", {})
        ok_resp = responses.get("200") or responses.get("201") or {}
        if not isinstance(ok_resp, dict):
            return {}
        # OAS 3.x
        content = ok_resp.get("content", {})
        if content:
            first_media = next(iter(content.values()), {})
            schema = first_media.get("schema", {})
            return {"schema_type": schema.get("type"), "schema": schema}
        # OAS 2.x
        schema = ok_resp.get("schema", {})
        return {"schema_type": schema.get("type"), "schema": schema}
