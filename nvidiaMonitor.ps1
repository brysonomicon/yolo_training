function NvidiaMonitor([int]$deviceId)
{
  nvidia-smi `
    --query `
    --id=$deviceId `
    --display=TEMPERATURE `
    --loop
}

