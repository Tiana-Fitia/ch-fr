# -*- coding: utf-8 -*-
"""
Advanced example of AI Optimizer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from stream_optimizer import AdvancedOptimizer
import logging
from sklearn.datasets import make_classification
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def advanced_example():
    """Advanced usage example"""
    logger.info("=== Advanced AI Optimizer Example ===")
    
    # Create config
    config = Config()
    
    # Create advanced optimizer
    optimizer = AdvancedOptimizer(config)
    
    # Generate more complex test data
    logger.info("Generating complex test data...")
    X, y = make_classification(
        n_samples=200,
        n_features=15,
        n_informative=10,
        n_redundant=3,
        n_clusters_per_class=2,
        random_state=42
    )
    
    logger.info("Data shape: " + str(X.shape))
    logger.info("Classes: " + str(np.unique(y)))
    
    # Advanced optimization with CV
    logger.info("\n=== Starting Advanced Optimization ===")
    result = optimizer.optimize_with_cv(X, y, cv_folds=3)
    
    # Display results
    logger.info("\n=== Results ===")
    logger.info("Best model: " + result.model_name)
    logger.info("Best score: " + str(result.best_score))
    logger.info("Optimization time: " + str(result.optimization_time) + "s")
    
    # Model comparison
    logger.info("\n=== Model Comparison ===")
    comparisons = optimizer.compare_models(X, y)
    
    for i, comp in enumerate(comparisons):
        logger.info(str(i+1) + ". " + comp['model_name'] + ": " + str(comp['accuracy']))
    
    # Detailed report
    report = optimizer.get_optimization_report()
    logger.info(report)
    
    # Save results
    result.save("results/advanced_results.json")
    logger.info("\nResults saved to results/advanced_results.json")
    
    # Save comparison
    with open("results/model_comparison.txt", "w") as f:
        f.write(report)
    
    logger.info("=== Advanced example completed! ===")

if __name__ == "__main__":
    advanced_example()
