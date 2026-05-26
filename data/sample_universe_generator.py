"""
data/sample_universe_generator.py - Sample universe template generator.

Generates top50 / top100 / top200 profile template CSVs from the
config/universe/ sample files, without fabricating price data.

Usage:
    from data.sample_universe_generator import SampleUniverseGenerator
    gen = SampleUniverseGenerator()
    gen.generate('top50', output_path='data/import/profile/stock_profile.csv')
    info = gen.describe('top100')
"""

import os
import logging

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_TEMPLATE_PATHS = {
    'top50':  os.path.join(_BASE_DIR, 'config', 'universe', 'top50_sample.csv'),
    'top100': os.path.join(_BASE_DIR, 'config', 'universe', 'top100_sample.csv'),
    'top200': os.path.join(_BASE_DIR, 'config', 'universe', 'top200_sample.csv'),
}


class SampleUniverseGenerator:
    """Reads sample universe templates and optionally writes them to output paths."""

    def generate(self, template: str = 'top50', output_path: str = None) -> dict:
        """
        Read a sample template and write it to output_path.

        Does NOT generate price data. Only produces profile schema rows.

        Returns summary dict with rows count and output path.
        """
        import pandas as pd

        if template not in _TEMPLATE_PATHS:
            return {'success': False, 'error': f"Unknown template: {template}"}

        tpath = _TEMPLATE_PATHS[template]
        if not os.path.isfile(tpath):
            return {'success': False, 'error': f"Template not found: {tpath}"}

        encodings = ['utf-8-sig', 'utf-8', 'big5', 'cp950']
        df = None
        for enc in encodings:
            try:
                df = pd.read_csv(tpath, dtype={'symbol': str}, encoding=enc)
                break
            except UnicodeDecodeError:
                continue
            except Exception as exc:
                return {'success': False, 'error': str(exc)}

        if df is None:
            return {'success': False, 'error': f"Cannot decode {tpath}"}

        df['symbol'] = df['symbol'].astype(str).str.strip()

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            logger.info("SampleUniverseGenerator: wrote %d rows to %s", len(df), output_path)

        return {
            'success': True,
            'template': template,
            'source': tpath,
            'output': output_path,
            'rows': len(df),
            'symbols': df['symbol'].tolist(),
        }

    def describe(self, template: str = 'top50') -> dict:
        """Return metadata about a template without writing anything."""
        result = self.generate(template, output_path=None)
        return result
