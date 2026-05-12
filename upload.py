import wandb

# Use the 'id' of the old run and set resume="must"
wandb.init(
    project="guitar-train-clean", 
    entity="hubert322-hubert-hung",
    id="eqxsyz74",   # This is the ID from your URL
    resume="must"    # This ensures you don't start a new run
)

# Now it saves directly to that existing run
# Create the artifact object
model_artifact = wandb.Artifact('guitar-model-step-13500', type='model')

# Add your file to it
model_artifact.add_file("step-13500.ckpt")

# Log it!
wandb.log_artifact(model_artifact)

