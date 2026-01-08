# -*- coding: utf-8 -*-
"""
Ultra simple optimizer without external dependencies
"""

import random
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleOptimizer:
    """Ultra simple optimizer that works without numpy/sklearn"""
    
    def __init__(self):
        self.models = []
        self.best_model = None
        self.results = []
    
    def create_mock_data(self, n_samples=100, n_features=5):
        """Create mock data without numpy"""
        logger.info("Creating mock data...")
        
        data = []
        target = []
        
        for i in range(n_samples):
            # Create random features
            features = [random.random() * 10 for _ in range(n_features)]
            
            # Create target based on simple rule (for testing)
            target_value = 1 if sum(features) > n_features * 5 else 0
            
            data.append(features)
            target.append(target_value)
        
        logger.info("Created " + str(len(data)) + " samples with " + str(len(data[0])) + " features")
        return data, target
    
    def simple_model_predict(self, features, model_type="random"):
        """Simple prediction without real ML models"""
        if model_type == "random":
            # Random predictions (for testing)
            return random.choice([0, 1])
        elif model_type == "threshold":
            # Simple threshold-based prediction
            return 1 if sum(features) > len(features) * 5 else 0
        elif model_type == "majority":
            # Always predict majority class
            return 1
    
    def evaluate_model(self, data, target, model_type):
        """Simple evaluation without sklearn"""
        correct = 0
        total = len(data)
        
        for i in range(total):
            prediction = self.simple_model_predict(data[i], model_type)
            if prediction == target[i]:
                correct += 1
        
        accuracy = float(correct) / total
        return accuracy
    
    def optimize_models(self, data, target):
        """Test different simple models"""
        logger.info("Starting simple optimization...")
        
        model_types = ["random", "threshold", "majority"]
        
        for model_type in model_types:
            logger.info("Testing " + model_type + " model...")
            
            accuracy = self.evaluate_model(data, target, model_type)
            
            result = {
                'model_name': model_type,
                'accuracy': accuracy,
                'correct_predictions': int(accuracy * len(data))
            }
            
            self.results.append(result)
            logger.info("  Accuracy: " + str(accuracy))
        
        # Find best model
        best_result = max(self.results, key=lambda x: x['accuracy'])
        self.best_model = best_result
        
        logger.info("Best model: " + best_result['model_name'])
        logger.info("Best accuracy: " + str(best_result['accuracy']))
        
        return best_result
    
    def save_results(self, filepath):
        """Save results to JSON"""
        output = {
            'best_model': self.best_model,
            'all_results': self.results,
            'total_models_tested': len(self.results)
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info("Results saved to " + filepath)

def run_simple_example():
    """Run simple example"""
    logger.info("=== Simple AI Optimizer Example ===")
    
    # Create optimizer
    optimizer = SimpleOptimizer()
    
    # Create mock data
    data, target = optimizer.create_mock_data(n_samples=50, n_features=5)
    
    # Optimize models
    best_result = optimizer.optimize_models(data, target)
    
    # Save results
    optimizer.save_results("results/simple_results.json")
    
    # Print summary
    print "\n" + "="*40
    print "    OPTIMIZATION SUMMARY"
    print "="*40
    print "Best Model: " + best_result['model_name']
    print "Best Accuracy: " + str(best_result['accuracy'])
    print "Total Models Tested: " + str(len(optimizer.results))
    print "="*40
    
    logger.info("Simple example completed!")

if __name__ == "__main__":
    run_simple_example()
