import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import re

class CleanCSV(beam.DoFn):
    def process(self, element):
        import csv
        from io import StringIO

        # Use CSV parser to handle commas inside quotes
        reader = csv.DictReader(StringIO(element))
        for row in reader:
            try:
                # Validation: Check required fields
                if not row['name'] or not row['age'] or not row['email']:
                    return  # skip malformed rows

                # Clean: Capitalize name properly
                name = row['name'].strip().title()

                # Validate age
                age = int(row['age'])
                if age < 18:
                    return  # skip minors

                # Validate email format
                email = row['email'].strip().lower()
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    return  # skip invalid emails

                yield {
                    'name': name,
                    'age': age,
                    'email': email
                }

            except Exception as e:
                # Log or handle parsing issues
                return  # skip bad record

# Set pipeline options
options = PipelineOptions(
    project='your-project-id',
    region='your-region',
    runner='DataflowRunner',
    temp_location='gs://your-bucket/temp',
    staging_location='gs://your-bucket/staging',
    save_main_session=True  # useful for some packages in Dataflow
)

# Build the pipeline
with beam.Pipeline(options=options) as p:
    (
        p
        | 'Read CSV' >> beam.io.ReadFromText('gs://your-bucket/input.csv', skip_header_lines=1)
        | 'Clean and Transform' >> beam.ParDo(CleanCSV())
        | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
            'your_dataset.your_table',
            schema='name:STRING, age:INTEGER, email:STRING',
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )
