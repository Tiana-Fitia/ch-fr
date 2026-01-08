# -*- coding: utf-8 -*-
"""
Stream Optimizer - Advanced version
Enhanced ML model optimization
"""

import numpy as np
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score

logger = logging.getLogger(__name__)

class OptimizationResult:
    """Optimization result"""
    def __init__(self, best_params, best_score, model_name, metrics, optimization_time=0.0):
        self.best_params = best_params
        self.best_score = best_score
        self.model_name = model_name
        self.metrics = metrics
        self.optimization_time = optimization_time
    
    def save(self, filepath):
        """Save results"""
        import json
        results = {
            'best_params': self.best_params,
            'best_score': self.best_score,
            'model_name': self.model_name,
            'metrics': self.metrics,
            'optimization_time': self.optimization_time
        }
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)

class AdvancedOptimizer:
    """Advanced ML model optimizer"""
    
    def __init__(self, config):
        self.config = config
        self.models = {}
        self.best_model = None
        self.results_history = []
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize models with different parameters"""
        self.models = {
            'random_forest_tuned': RandomForestClassifier(
                n_estimators=150, max_depth=7, random_state=42
            ),
            'random_forest_simple': RandomForestClassifier(
                n_estimators=100, max_depth=5, random_state=42
            ),
            'gradient_boosting_tuned': GradientBoostingClassifier(
                n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42
            ),
            'gradient_boosting_simple': GradientBoostingClassifier(
                n_estimators=50, learning_rate=0.3, max_depth=3, random_state=42
            )
        }
    
    def optimize_with_cv(self, X, y, cv_folds=5):
        """Optimize with cross-validation"""
        import time
        start_time = time.time()
        
        best_score = -999999
        best_result = None
        
        logger.info("Starting optimization with " + str(cv_folds) + " folds CV")
        
        for model_name, model in self.models.items():
            logger.info("Testing " + model_name + "...")
            
            # Cross-validation
            cv_scores = cross_val_score(model, X, y, cv=cv_folds, scoring='accuracy')
            mean_score = cv_scores.mean()
            std_score = cv_scores.std()
            
            logger.info("  CV Score: " + str(mean_score) + " (+/- " + str(std_score) + ")")
            
            # Fit model for metrics calculation
            model.fit(X, y)
            y_pred = model.predict(X)
            
            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(y, y_pred),
                'precision': precision_score(y, y_pred, average='weighted'),
                'recall': recall_score(y, y_pred, average='weighted'),
                'cv_mean': mean_score,
                'cv_std': std_score
            }
            
            result = OptimizationResult(
                best_params=model.get_params(),
                best_score=mean_score,
                model_name=model_name,
                metrics=metrics,
                optimization_time=time.time() - start_time
            )
            
            self.results_history.append(result)
            
            if result.best_score > best_score:
                best_score = result.best_score
                best_result = result
                self.best_model = model
        
        logger.info("Optimization completed!")
        logger.info("Best model: " + best_result.model_name)
        logger.info("Best CV score: " + str(best_result.best_score))
        
        return best_result
    
    def get_optimization_report(self):
        """Get detailed optimization report"""
        if not self.results_history:
            return "No optimization results available"
        
        report = "\n=== OPTIMIZATION REPORT ===\n"
        for i, result in enumerate(self.results_history):
            report += "\nModel " + str(i+1) + ": " + result.model_name + "\n"
            report += "  Score: " + str(result.best_score) + "\n"
            report += "  Accuracy: " + str(result.metrics.get('accuracy', 'N/A')) + "\n"
            report += "  Precision: " + str(result.metrics.get('precision', 'N/A')) + "\n"
            report += "  Recall: " + str(result.metrics.get('recall', 'N/A')) + "\n"
        
        best_result = max(self.results_history, key=lambda x: x.best_score)
        report += "\n=== BEST MODEL ===\n"
        report += "Model: " + best_result.model_name + "\n"
        report += "Score: " + str(best_result.best_score) + "\n"
        
        return report
    
    def compare_models(self, X, y):
        """Compare all models and return rankings"""
        results = []
        
        for model_name, model in self.models.items():
            logger.info("Evaluating " + model_name + "...")
            
            # Simple train-test split for comparison
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            
            results.append({
                'model_name': model_name,
                'accuracy': accuracy,
                'params': model.get_params()
            })
        
        # Sort by accuracy
        results.sort(key=lambda x: x['accuracy'], reverse=True)
        
        return results
