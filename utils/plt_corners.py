import matplotlib.pyplot as plt
import numpy as np
import sys


def click_corners(image: np.ndarray) -> np.ndarray:
    """
    Allow the user to click on four points on the provided image to define corners.
    This is useful for manually defining the corners of the 
    projector image when doing data collection since the
    automated contour-based system doesn't always do a good
    job in all environments.
    
    Parameters:
    - image (np.ndarray): The recorded image, want to select 
        corners in image representing edges of projector image.
    
    Returns:
    - np.ndarray: An array containing the selected corner points.
    """

    selected_points = []

    def onclick(event):
        """
        Handle mouse click events. When the right mouse button (3)
        is pressed , show the points on the plot. When 4 points
        are selected, stop the interaction.

        Parameters:
        - event: The mouse click event.
        """
        if event.button == 3:
            x = int(event.xdata)
            y = int(event.ydata)
            selected_points.append((x, y))
            plt.scatter(x, y, color='r')
            plt.draw()

            if len(selected_points) == 4:
                plt.disconnect(cid)
                plt.close()

    # Display the image, with interactive zooming and panning and onclick function
    plt.imshow(image)
    plt.title('Right click to select 4 points')
    plt.axis('on')
    plt.gca().set_autoscale_on(True)
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    # Print and return selected points
    print("Selected points:", selected_points)
    if len(selected_points) != 4:
        raise Exception("4 points were not selected")
    selected_points = np.array(selected_points, dtype=np.float32)
    return selected_points

def check_corners(image, selected_points):
    """
    Show the selected points on the image.

    Parameters:
    - image (np.ndarray): the recorded image
    - points (np.ndarray): points representing corners of projector image
    """

    def onclick(event):
        """
        Handle mouse click events. When the left mouse button (1)
        is pressed, continue the code elsewhere by returning.
        Otherwise, stop with sys.exit.

        Parameters:
        - event: The mouse click event.
        """
        plt.disconnect(cid)
        plt.close()
        if event.button == 1:
            print("Returing")
            return
        else:
            print("Exiting")
            sys.exit()
                
    img_copy = image.copy()
    plt.imshow(img_copy)
    for point in selected_points:
        plt.scatter(point[0], point[1], color='r', s=100)
    
    # Display the image, with interactive zooming and panning and onclick function
    plt.title("Selected points. Left click to confirm, right click to exit.")
    plt.axis('on')
    plt.gca().set_autoscale_on(True)
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    