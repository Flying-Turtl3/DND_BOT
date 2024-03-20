# DND BOT
## Character Creation Bot for Dungeons and Dragons 5e

This is a DnD creation bot which uses GPT-4 to generate a character including backstory, class, race and helps to answer user questions along the way. 
A notebook walks through all the steps and prompts. 
An Autogen folder contains an agentic workflow where each character creation concept like backstoty, class, race are each delegated to a single agent. The agents then work together through a group chat to complete the task. Function calling is currently partially implemented to read character attributes from a DB to provide deterministic outputs into the GPT response. 
