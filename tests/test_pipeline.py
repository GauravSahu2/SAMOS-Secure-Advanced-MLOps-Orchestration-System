import unittest
import pandas as pd
import os
import sys

# Add src to path
sys.path.append('src')

class TestMLPipeline(unittest.TestCase):
    def test_pii_masking(self):
        """Verify Phase 3: PII Masking logic."""
        from data_ops.mask_pii import mask_pii
        test_data = pd.DataFrame({'email': ['test@example.com']})
        test_data.to_csv('test_email.csv', index=False)
        
        mask_pii('test_email.csv', 'test_email_masked.csv')
        df = pd.read_csv('test_email_masked.csv')
        
        self.assertIn('***@', df['email'][0])
        os.remove('test_email.csv')
        os.remove('test_email_masked.csv')

    def test_validation_logic(self):
        """Verify Phase 2: Range Validation."""
        from data_ops.validate import validate_data
        test_data = pd.DataFrame({'age': [200], 'income': [1000]})
        test_data.to_csv('test_val.csv', index=False)
        
        validate_data('test_val.csv', 'test_clean.csv', 'test_dlq.csv')
        dlq_df = pd.read_csv('test_dlq.csv')
        
        self.assertEqual(len(dlq_df), 1)
        os.remove('test_val.csv')
        os.remove('test_clean.csv')
        os.remove('test_dlq.csv')

if __name__ == '__main__':
    unittest.main()
