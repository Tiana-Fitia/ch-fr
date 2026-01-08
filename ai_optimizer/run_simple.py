# -*- coding: utf-8 -*-
"""
Simple run without external dependencies
"""

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_simple():
    """Run simple version"""
    logger.info("🚀 Starting simple AI optimizer (no dependencies)...")
    
    # Run simple example
    logger.info("Step 1: Running simple optimization...")
    os.system("python examples/simple_optimizer.py")
    
    logger.info("\n✅ Simple optimization completed!")
    logger.info("Results saved in results/simple_results.json")

if __name__ == "__main__":
    run_simple()
