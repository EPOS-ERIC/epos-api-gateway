import os
import base64
import requests
from flask import request, Response
import logging

logger = logging.getLogger(__name__)


def layers_eurogeographics(type):
    try:
        token_base64 = os.getenv("EUROGEOGRAPHICS_TOKEN", "SW1WMWNtOW5aVzluY21Gd2FHbGpjMTl5WldkcGMzUmxjbVZrWHpneE1USTRPU0kuSFkwb3V3LlktelBJMmh5TTFLZmlvRE9CV1lIdHN6Sm9UVQ==")

        if not token_base64:
            logger.error("EUROGEOGRAPHICS_TOKEN is not configured")
            return Response(
                '{"error": "EuroGeographics token is not configured"}',
                status=500,
                content_type="application/json",
            )

        try:
            token = base64.b64decode(token_base64).decode("utf-8")
        except Exception:
            logger.exception("Invalid base64 value in EUROGEOGRAPHICS_TOKEN")
            return Response(
                '{"error": "Invalid EuroGeographics token configuration"}',
                status=500,
                content_type="application/json",
            )

        domains = {
            "maps": "https://www.mapsforeurope.org/maps/wms",
            "pan-european-imagery": (
                "https://www.mapsforeurope.org/api/v2/maps/external/wms/"
                "pan-european-imagery"
            ),
        }

        target_url = domains.get(type)

        if not target_url:
            return Response(
                '{"error": "Invalid type"}',
                status=400,
                content_type="application/json",
            )

        params = request.args.to_dict(flat=False)
        params["token"] = token

        wms_response = requests.get(
            target_url,
            params=params,
            timeout=60,
        )

        return Response(
            wms_response.content,
            status=wms_response.status_code,
            content_type=wms_response.headers.get(
                "Content-Type",
                "application/octet-stream",
            ),
        )

    except requests.exceptions.ConnectionError:
        return Response(
            '{"error": "Cannot connect to EuroGeographics service"}',
            status=503,
            content_type="application/json",
        )

    except requests.exceptions.Timeout:
        return Response(
            '{"error": "EuroGeographics service timeout"}',
            status=504,
            content_type="application/json",
        )

    except requests.exceptions.RequestException:
        logger.exception("EuroGeographics WMS request failed")
        return Response(
            '{"error": "EuroGeographics request failed"}',
            status=502,
            content_type="application/json",
        )

    except Exception:
        logger.exception("Unexpected error in layers_eurogeographics")
        return Response(
            '{"error": "Internal server error"}',
            status=500,
            content_type="application/json",
        )