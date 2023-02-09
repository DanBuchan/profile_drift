#!/bin/bash -l
#$ -o /home/ucbcdwb/Scratch/output/profile/srd.out
#$ -e /home/ucbcdwb/Scratch/output/profile/srd.err

# Batch script to run a serial array job under SGE.
# Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=1:00:0

# Request 1 gigabyte of RAM (must be an integer followed by M, G, or T)
#$ -l mem=1G

# Request 15 gigabyte of TMPDIR space (default is 10 GB - remove if cluster is diskless)
#$ -l tmpfs=10G

# Set up the job array.  In this instance we have requested 10000 tasks
# numbered 1 to 10000.
#$ -t 1-1

# Set the name of the job.
#$ -N pfamReps

# Set the working directory to somewhere in your scratch space.
# Replace "<your_UCL_id>" with your UCL user ID :)
#$ -wd /home/ucbcdwb/Scratch/output/profile/

# Run the application.
source /home/ucbcdwb/Scratch/profile_drift/profile_drift/bin/activate
echo "python run_pfam_rep_blasts.py ~/Scratch/Data/pfam/reps.fasta.fa ~/Scratch/Data/pfam/pfam_fasta.fa $JOB_NAME $SGE_TASK_ID"
