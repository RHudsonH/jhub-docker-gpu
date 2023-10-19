# GPU Allocator #
This is a simple api to track GPUs available on a system and wether or not they're allocated.

## Why is this needed? ##
The way docker allocates GPU resources doesn't allow us to request a number of GPUs. Instead we have to request specific GPUs either by enumeration position or by UUID. So we need a way to track which GPUs have been allocated and prevent over suscription.

## How does it work ##

## What still needs to be done? ##

## Future feature ideas ##