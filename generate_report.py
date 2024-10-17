import boto3
import configparser
import datetime
import pandas as pd
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError

def get_profiles():
    """Retrieve AWS profiles and regions from AWS config."""
    print("I AM IN GET PROFILE")
    all_profiles = {}
    config = configparser.ConfigParser()
    
   """ if not os.path.exists('/root/.aws'):
        print("Current working directory:", os.getcwd())
        print("Config file does not exist.")
        return all_profiles """

    config.read(os.path.expanduser('/root/.aws/config'))
    #config.read('/var/lib/jenkins/.aws/config')

    print("AFTER CONFIG FILE READ")

    for profile in config.sections():
        print(f"These are the profile in for loop: {profile}")
        
        profile_region = config.get(profile, 'region', fallback=config.get('default', 'region'))
        all_profiles[profile] = profile_region

    return all_profiles

def get_instance_metrics(profile, region, instance_id):
    """Get EC2 metrics using CloudWatch."""
    session = boto3.Session(profile_name=profile, region_name=region)
    cloudwatch_client = session.client('cloudwatch')

    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(days=7)  # Metrics from the last week
    period = 3600  # Data every hour

    # Get CPU Utilization
    cpu_utilization = get_metric_statistics(cloudwatch_client, instance_id, 'CPUUtilization', 'AWS/EC2', period, start_time, end_time)

    # Get Memory Utilization (Requires CloudWatch Agent)
    memory_utilization = get_metric_statistics(cloudwatch_client, instance_id, 'mem_used_percent', 'CWAgent', period, start_time, end_time)

    return {
        'CPU Utilization': cpu_utilization,
        'Memory Utilization': memory_utilization,
    }

def get_metric_statistics(cloudwatch_client, instance_id, metric_name, namespace, period, start_time, end_time):
    """Retrieve statistics for a specific metric from CloudWatch."""
    try:
        response = cloudwatch_client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=['Average']
        )

        if 'Datapoints' in response and response['Datapoints']:
            return response['Datapoints'][0].get('Average', 'N/A')
        else:
            print(f"No data found for metric {metric_name} for instance {instance_id}")
            return 'N/A'
    except (NoCredentialsError, PartialCredentialsError, BotoCoreError) as e:
        print(f"Error fetching metric {metric_name} for instance {instance_id}: {e}")
        return 'N/A'

def get_all_instances(profile, region):
    """Retrieve all EC2 instance IDs for a given profile and region."""
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2_client = session.client('ec2')

    try:
        response = ec2_client.describe_instances()
        instances = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]
        return instances
    except (NoCredentialsError, PartialCredentialsError, BotoCoreError) as e:
        print(f"Error retrieving instances for profile {profile}: {e}")
        return []

def export_to_excel(data, filename='/app/reports/ec2_metrics_report.xlsx'):
    """Export EC2 metrics data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename}")
    return filename

if __name__ == "__main__":
    all_profiles = get_profiles()
    metrics_report = []

    print("AWS config path:", os.path.expanduser('~/.aws/config'))
    
    # Get the current working directory
    current_directory = os.getcwd()
    print(f"current_directory: {current_directory}")

# List all directories in the current directory
    #directories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
    
    root_dir = '/root'  # Specify the directory to walk through

    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f"Directory: {dirpath}")
        for dirname in dirnames:
            print(f"Subdirectory: {os.path.join(dirpath, dirname)}")
        for filename in filenames:
            print(f"File: {os.path.join(dirpath, filename)}")

    print(f"These are the profile: {all_profiles}")
    for profile, region in all_profiles.items():
        print(f"Collecting metrics for profile: {profile} in region: {region}")
        instance_ids = get_all_instances(profile, region)
        print(f"Instance IDs for profile {profile}: {instance_ids}")

        for instance_id in instance_ids:
            metrics = get_instance_metrics(profile, region, instance_id)
            print(f"Metrics for instance {instance_id}: {metrics}")
            metrics_report.append({
                'Profile': profile,
                'Region': region,
                'Instance ID': instance_id,
                'CPU Utilization': metrics['CPU Utilization'],
                'Memory Utilization': metrics['Memory Utilization'],
            })

    


    #print("Directories in the current directory:", directories)

    # Before exporting the report
    print("Metrics report data:", metrics_report)

    # Export the report to Excel
    report_file = export_to_excel(metrics_report)

    # Send the report via email
    recipient_email = "londhe.karishma61@gmail.com"  # Replace with the recipient's email
   # send_email("EC2 Metrics Weekly Report", "Please find the attached EC2 metrics report.", recipient_email, report_file)
