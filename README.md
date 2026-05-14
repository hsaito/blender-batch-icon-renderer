
# **Batch Icon Renderer (Blender Add‑on)**

A Blender add‑on for generating multiple icon‑sized PNG renders in a single, reliable batch.  
It is designed primarily for Windows icon workflows but works for any pipeline that requires consistent multi‑resolution outputs.

## **Features**

- **Batch‑render multiple icon sizes** from a single camera view  
- **Sequential, event‑driven rendering** using Blender’s `render_complete` handler  
- **No race conditions, no skipped sizes, no UI lockups**  
- **Automatic file naming**:  
  ```
  {prefix}{size}.png
  ```
  Example: `icon256.png`
- **Blend‑relative paths supported** (e.g., `//icons/`)  
- Integrated into the **N‑panel** under **Icon Render**

## **Supported Icon Sizes (Windows Standard)**

The add‑on includes all commonly used Windows icon resolutions:

- **512 × 512**  
- **256 × 256**  
- **128 × 128**  
- **96 × 96**  
- **64 × 64**  
- **48 × 48**  
- **40 × 40**  
- **32 × 32**  
- **24 × 24**  
- **20 × 20**  
- **16 × 16**

Each size can be enabled or disabled individually.

## **How It Works**

1. Set a **file name prefix** (e.g., `icon`)  
2. Choose a **save directory**  
3. Select the icon sizes you want to generate  
4. Click **Render Icons**  

The add‑on will:

- Adjust the render resolution  
- Render the image  
- Save it as a PNG  
- Wait for Blender’s render completion event  
- Move on to the next size  

This ensures **stable, ordered, and fully deterministic batch rendering**.

## **Why This Add‑on Exists**

Rendering icons manually in Blender is slow and error‑prone.  
Naively looping through resolutions can cause:

- UI freezes  
- Skipped renders  
- Overwritten files  
- Race‑condition‑like behavior  

This add‑on solves those issues by using Blender’s event system to synchronize each render step, ensuring that **each resolution is rendered only after the previous one has fully completed**.

## **Usage**

1. Frame your object with the active camera  
2. Open the **Icon Render** tab in the N‑panel  
3. Enter a prefix and save directory  
4. Select the icon sizes you want  
5. Press **Render Icons**  

Your PNG files will be generated automatically in the selected folder.

## **Future Enhancements**

Potential future additions include:

- macOS icon size presets  
- iOS / Android app icon presets  
- Automatic `.ico` file generation  
- Multi‑camera batch rendering  
- Preset groups (Windows / macOS / Mobile)
