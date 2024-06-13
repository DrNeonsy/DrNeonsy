# Guide

>[!NOTE]
This guide is based on how I tend do it, so if you don't want to loose your extensions or profiles, you'll need to adjust accordingly.

1. Locate your `.vscode` directory. It should be in your home directory (`~` | `%userprofile%`).

2. Remove the `extensions` and `extensions.json` files. You can also just remove the entire directory.

3. Locate your `User` directory. For `windows`, this should be under `%appdata%` as either the `Code` directory.

4. Remove the contents of the `User` directory.

5. Open `VSCode` and import the default profile.

6. Close your editor and move everything from the newly created profile from the `profiles` directory to the `User` one.

>[!NOTE]
You can now remove the profiles directory

7. If you've followed step `6.`, you should also have the `extensions.json` file in the `Users` directory. Move that to the in step `1.` mentioned directory under extensions.

8. You can now open your editor again and remove the imported default profile.

9. If all went as expected, you should have the default profile as your actual default and not in a separate profile. You can now import the other profiles as needed.