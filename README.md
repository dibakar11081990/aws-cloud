<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 1000px;
      margin: 0 auto;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
      padding: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 10px;
      color: white;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header h1 {
      margin: 0;
      font-size: 2.5em;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .header p {
      margin: 10px 0 0;
      font-size: 1.2em;
      opacity: 0.9;
    }
    .section {
      margin-bottom: 30px;
      background: white;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .section-header {
      background: linear-gradient(to right, #5e35b1, #3949ab);
      color: white;
      padding: 15px 20px;
      font-size: 1.3em;
      margin: 0;
      display: flex;
      align-items: center;
    }
    .section-header .icon {
      margin-right: 10px;
      font-size: 1.5em;
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th {
      background-color: #f8f9fa;
      padding: 12px 15px;
      text-align: left;
      font-weight: 600;
      color: #333;
      border-bottom: 2px solid #ddd;
    }
    td {
      padding: 12px 15px;
      border-bottom: 1px solid #eee;
    }
    tr:hover {
      background-color: #f5f5f5;
    }
    .aws {
      color: #FF9900;
      font-weight: 500;
    }
    .azure {
      color: #0078D4;
      font-weight: 500;
    }
    .gcp {
      color: #4285F4;
      font-weight: 500;
    }
    .use-case {
      font-weight: 500;
      color: #555;
    }
    .footer {
      text-align: center;
      margin-top: 30px;
      color: #666;
      font-size: 0.9em;
    }
    .cloud-logos {
      display: flex;
      justify-content: center;
      margin-top: 15px;
    }
    .cloud-logo {
      width: 40px;
      height: 40px;
      margin: 0 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
    }
    .aws-logo {
      background-color: #FF9900;
      color: white;
    }
    .azure-logo {
      background-color: #0078D4;
      color: white;
    }
    .gcp-logo {
      background-color: #4285F4;
      color: white;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Cloud Tools for Data Engineers</h1>
      <p>Comparison of AWS, Azure, and GCP Solutions</p>
      <div class="cloud-logos">
        <div class="cloud-logo aws-logo">AWS</div>
        <div class="cloud-logo azure-logo">AZ</div>
        <div class="cloud-logo gcp-logo">GCP</div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header"><span class="icon">📦</span> Data Storage & Data Lakes</h2>
      <table>
        <tr>
          <th width="25%">Use Case</th>
          <th width="25%">AWS</th>
          <th width="25%">Azure</th>
          <th width="25%">GCP</th>
        </tr>
        <tr>
          <td class="use-case">Object Storage</td>
          <td class="aws">S3</td>
          <td class="azure">Blob Storage</td>
          <td class="gcp">Cloud Storage</td>
        </tr>
        <tr>
          <td class="use-case">Data Lake</td>
          <td class="aws">Lake Formation</td>
          <td class="azure">Data Lake Storage Gen2</td>
          <td class="gcp">Cloud Storage + Dataplex</td>
        </tr>
        <tr>
          <td class="use-case">Managed HDFS</td>
          <td class="aws">EMR File System (EMRFS)</td>
          <td class="azure">HDInsight</td>
          <td class="gcp">Dataproc</td>
        </tr>
      </table>
    </div>

    <div class="section">
      <h2 class="section-header"><span class="icon">⚙️</span> Data Processing</h2>
      <table>
        <tr>
          <th width="25%">Use Case</th>
          <th width="25%">AWS</th>
          <th width="25%">Azure</th>
          <th width="25%">GCP</th>
        </tr>
        <tr>
          <td class="use-case">Batch Processing</td>
          <td class="aws">AWS Batch, EMR</td>
          <td class="azure">Azure Batch, HDInsight</td>
          <td class="gcp">Dataflow, Dataproc</td>
        </tr>
        <tr>
          <td class="use-case">Stream Processing</td>
          <td class="aws">Kinesis Data Analytics</td>
          <td class="azure">Stream Analytics</td>
          <td class="gcp">Dataflow</td>
        </tr>
        <tr>
          <td class="use-case">Serverless ETL</td>
          <td class="aws">Glue</td>
          <td class="azure">Data Factory</td>
          <td class="gcp">Cloud Data Fusion, Dataflow</td>
        </tr>
        <tr>
          <td class="use-case">Workflow Orchestration</td>
          <td class="aws">Step Functions, MWAA</td>
          <td class="azure">Data Factory, Synapse Pipelines</td>
          <td class="gcp">Cloud Composer (Airflow)</td>
        </tr>
      </table>
    </div>

    <div class="section">
      <h2 class="section-header"><span class="icon">📊</span> Data Warehousing & Analytics</h2>
      <table>
        <tr>
          <th width="25%">Use Case</th>
          <th width="25%">AWS</th>
          <th width="25%">Azure</th>
          <th width="25%">GCP</th>
        </tr>
        <tr>
          <td class="use-case">Data Warehouse</td>
          <td class="aws">Redshift</td>
          <td class="azure">Synapse Analytics</td>
          <td class="gcp">BigQuery</td>
        </tr>
        <tr>
          <td class="use-case">Columnar Databases</td>
          <td class="aws">Redshift</td>
          <td class="azure">Synapse Analytics</td>
          <td class="gcp">BigQuery</td>
        </tr>
        <tr>
          <td class="use-case">Interactive Query</td>
          <td class="aws">Athena</td>
          <td class="azure">Synapse SQL Serverless</td>
          <td class="gcp">BigQuery</td>
        </tr>
        <tr>
          <td class="use-case">BI & Visualization</td>
          <td class="aws">QuickSight</td>
          <td class="azure">Power BI</td>
          <td class="gcp">Looker, Data Studio</td>
        </tr>
      </table>
    </div>

    <div class="section">
      <h2 class="section-header"><span class="icon">⚡</span> Streaming & Real-time</h2>
      <table>
        <tr>
          <th width="25%">Use Case</th>
          <th width="25%">AWS</th>
          <th width="25%">Azure</th>
          <th width="25%">GCP</th>
        </tr>
        <tr>
          <td class="use-case">Pub/Sub Messaging</td>
          <td class="aws">SNS, SQS</td>
          <td class="azure">Event Hubs, Service Bus</td>
          <td class="gcp">Pub/Sub</td>
        </tr>
        <tr>
          <td class="use-case">Stream Ingestion</td>
          <td class="aws">Kinesis Data Streams</td>
          <td class="azure">Event Hubs</td>
          <td class="gcp">Pub/Sub</td>
        </tr>
        <tr>
          <td class="use-case">Change Data Capture</td>
          <td class="aws">DMS</td>
          <td class="azure">Data Factory</td>
          <td class="gcp">Datastream</td>
        </tr>
      </table>
    </div>

    <div class="section">
      <h2 class="section-header"><span class="icon">🧠</span> Machine Learning Integration</h2>
      <table>
        <tr>
          <th width="25%">Use Case</th>
          <th width="25%">AWS</th>
          <th width="25%">Azure</th>
          <th width="25%">GCP</th>
        </tr>
        <tr>
          <td class="use-case">ML Platform</td>
          <td class="aws">SageMaker</td>
          <td class="azure">Azure Machine Learning</td>
          <td class="gcp">Vertex AI</td>
        </tr>
        <tr>
          <td class="use-case">ML Ops</td>
          <td class="aws">SageMaker</td>
          <td class="azure">Azure Machine Learning</td>
          <td class="gcp">Vertex AI</td>
        </tr>
        <tr>
          <td class="use-case">Feature Store</td>
          <td class="aws">SageMaker Feature Store</td>
          <td class="azure">Feature Store (preview)</td>
          <td class="gcp">Vertex AI Feature Store</td>
        </tr>
      </table>
    </div>

    <div class="section">
      <h2 class="section-header"><span class="icon">🔒</span> Governance & Security</h2>
      <table>
        <tr>
          <th width="25%">Use Case</th>
          <th width="25%">AWS</th>
          <th width="25%">Azure</th>
          <th width="25%">GCP</th>
        </tr>
        <tr>
          <td class="use-case">Data Catalog</td>
          <td class="aws">Glue Data Catalog</td>
          <td class="azure">Purview</td>
          <td class="gcp">Data Catalog</td>
        </tr>
        <tr>
          <td class="use-case">Data Governance</td>
          <td class="aws">Lake Formation</td>
          <td class="azure">Purview</td>
          <td class="gcp">Dataplex</td>
        </tr>
        <tr>
          <td class="use-case">Identity Management</td>
          <td class="aws">IAM</td>
          <td class="azure">Azure Active Directory</td>
          <td class="gcp">Cloud IAM</td>
        </tr>
        <tr>
          <td class="use-case">Data Security</td>
          <td class="aws">KMS, Macie</td>
          <td class="azure">Azure Information Protection</td>
          <td class="gcp">Cloud KMS, DLP API</td>
        </tr>
      </table>
    </div>

    <div class="footer">
      <p>Cloud Tools for Data Engineers - AWS vs Azure vs GCP Comparison - 2025</p>
    </div>
  </div>
</body>
</html>
