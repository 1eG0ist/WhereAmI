# WhereAmI

Telegram bot written in python. Designed to orient users around buildings. 

A system of roles has been implemented, for example, such as content maker, thanks to this role, a person will be able to add his building to the bot. 

The addition of the building takes place in several stages, the last of which is the addition of photos, with instructions, or signatures of the cabinets. 

Due to optimization, the part of the project responsible for the database is based on the idea of storing information in the form of graphs in order to avoid excessive data repeatability. 

The traversal of the graph located directly in the database is implemented. Each user has a list of favorite buildings. 

Users can add all the buildings that exist in the bot. Sorting them by city.
