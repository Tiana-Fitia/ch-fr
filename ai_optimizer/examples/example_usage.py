# -*- coding: utf-8 -*-
"""
Example usage of AI Optimizer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from stream_optimizer import StreamOptimizer
from predictor import Predictor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simple_example():
    """Simple usage example"""
    logger.info("=== AI Optimizer Example ===")
    
    # Create config
    config = Config()
    
    # Create optimizer
    optimizer = StreamOptimizer(config)
    
    # Simple test
    logger.info("Testing optimizer...")
    try:
        # Use our sample data
        result = optimizer.optimize_from_file("data/sample_data.csv")
        logger.info("Optimization completed!")
        logger.info("Best model: " + result.model_name)
        logger.info("Best score: " + str(result.best_score))
        
        # Save results
        result.save("results/example_results.json")
        logger.info("Results saved to results/example_results.json")
        
    except Exception as e:
        logger.error("Error in example: " + str(e))

if __name__ == "__main__":
    simple_example()
