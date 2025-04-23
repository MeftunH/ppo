"""
Real-world example of performance profiling in a data processing pipeline.
This simulates an ETL (Extract, Transform, Load) process with:
- Data extraction from multiple sources
- Complex data transformations
- Data validation
- Database operations
- Caching mechanisms
"""

import cProfile
import pstats
import time
import json
import random
from functools import lru_cache
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataRecord:
    id: int
    timestamp: datetime
    value: float
    metadata: Dict[str, str]


class DataSourceConnector:
    """Simulates external data source connections"""
    
    def __init__(self, source_name: str, latency: float = 0.1):
        self.source_name = source_name
        self.latency = latency
    
    def fetch_data(self, batch_size: int) -> List[Dict]:
        """Simulate fetching data from external source"""
        time.sleep(self.latency)  # Simulate network latency
        return [
            {
                "id": i,
                "timestamp": str(datetime.now()),
                "value": random.random() * 100,
                "metadata": {"source": self.source_name, "batch": str(batch_size)}
            }
            for i in range(batch_size)
        ]


class DataTransformer:
    """Handles data transformation and enrichment"""
    
    @lru_cache(maxsize=1000)
    def _calculate_complex_metric(self, value: float) -> float:
        """Expensive computation with caching"""
        time.sleep(0.01)  # Simulate complex calculation
        return value ** 2 * sum(1 / (i + 1) for i in range(100))
    
    def transform_record(self, record: Dict) -> DataRecord:
        """Transform raw data into structured record"""
        enriched_value = self._calculate_complex_metric(record["value"])
        return DataRecord(
            id=record["id"],
            timestamp=datetime.fromisoformat(record["timestamp"]),
            value=enriched_value,
            metadata=record["metadata"]
        )


class DataValidator:
    """Validates and filters data records"""
    
    def __init__(self):
        self.validation_cache = {}
    
    def is_valid(self, record: DataRecord) -> bool:
        """Validate record against business rules"""
        cache_key = f"{record.id}_{record.value}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        time.sleep(0.005)  # Simulate validation logic
        is_valid = (
            0 <= record.value <= 10000 and
            record.timestamp.year >= 2020 and
            "source" in record.metadata
        )
        self.validation_cache[cache_key] = is_valid
        return is_valid


class DatabaseManager:
    """Simulates database operations"""
    
    def __init__(self):
        self.db = {}
        self._batch_size = 100
        self._pending_records: List[DataRecord] = []
    
    def _bulk_insert(self):
        """Simulate bulk insert operation"""
        time.sleep(0.05)  # Simulate DB write
        for record in self._pending_records:
            self.db[record.id] = record
        self._pending_records = []
    
    def insert_record(self, record: DataRecord):
        """Insert record with batching support"""
        self._pending_records.append(record)
        if len(self._pending_records) >= self._batch_size:
            self._bulk_insert()
    
    def flush(self):
        """Force write pending records"""
        if self._pending_records:
            self._bulk_insert()


class DataPipeline:
    """Main data processing pipeline"""
    
    def __init__(self):
        self.sources = [
            DataSourceConnector("api_1", latency=0.1),
            DataSourceConnector("api_2", latency=0.15),
        ]
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.db = DatabaseManager()
    
    def process_batch(self, batch_size: int = 50):
        """Process a batch of data through the pipeline"""
        for source in self.sources:
            raw_data = source.fetch_data(batch_size)
            
            for raw_record in raw_data:
                # Transform
                record = self.transformer.transform_record(raw_record)
                
                # Validate
                if self.validator.is_valid(record):
                    # Store
                    self.db.insert_record(record)
        
        # Ensure all records are written
        self.db.flush()


def main():
    """Main function to run and profile the pipeline"""
    pipeline = DataPipeline()
    
    # Process multiple batches
    for _ in range(3):
        pipeline.process_batch(batch_size=50)


if __name__ == "__main__":
    # Run with profiling
    profiler = cProfile.Profile()
    profiler.enable()
    
    main()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    
    print("\nPerformance Profile:")
    print("-" * 60)
    
    # Sort by cumulative time and print top 20 functions
    stats.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)
    
    # Print callers of the slowest functions
    print("\nCallers of Top Functions:")
    print("-" * 60)
    stats.print_callers(10)