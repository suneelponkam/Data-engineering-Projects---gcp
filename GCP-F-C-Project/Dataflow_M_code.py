import apache_beam as beam
import gzip
import io

class CompressFile(beam.DoFn):
    def process(self, element):
        # Compress the file content using gzip
        compressed_content = gzip.compress(element.encode('utf-8'))

        # Write the compressed content to the output file (gzipped)
        output_file = element.replace('.csv', '.gz')  # Replace .csv with .gz for the compressed file
        yield (output_file, compressed_content)  # Yield as a tuple (filename, compressed content)

def run():
    # Define the pipeline options
    options = {
        'project': 'bright-antonym-436213-v2',
        'region': 'us-central1',
        'temp_location': 'gs://gfcp-bucket/temp/',  # Temporary directory for Dataflow operations
        'staging_location': 'gs://gfcp-bucket/',  # Staging directory for job components
    }

    # Create the pipeline
    with beam.Pipeline(options=options) as p:
        # Define the list of files to compress
        files_to_compress = ['gs://gfcp-bucket/my-source-bucket/sample_data.csv']

        # Read the files and apply the compression logic
        (p
         | 'Read Files' >> beam.Create(files_to_compress)
         | 'Compress Files' >> beam.ParDo(CompressFile())
         | 'Write Compressed Files' >> beam.io.WriteToText(
             'gs://gfcp-bucket/my-destination-bucket/compressed_file',
             file_name_suffix='.gz',
             shard_name_template='',
             coder=beam.coders.BytesCoder()
         )
        )

if __name__ == '__main__':
    run()
