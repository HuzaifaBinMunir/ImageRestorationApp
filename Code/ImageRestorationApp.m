classdef ImageRestorationApp < handle
    properties
        degradedImage
        restoredImage
        fig
        degradedAxes
        restoredAxes
    end
    
    methods
        function app = ImageRestorationApp()
            % Create the main figure
            app.fig = uifigure('Name', 'Image Restoration App', 'Position', [100 100 800 400]);
            
            % Create a control panel
            controlPanel = uipanel(app.fig, 'Title', 'Controls', 'Position', [20 100 200 200]);
            
            % Load button
            uibutton(controlPanel, 'Text', 'Load Degraded Image', 'Position', [20 130 150 30], ...
                'ButtonPushedFcn', @(~, ~) app.loadImage());
            
            % Restore button
            uibutton(controlPanel, 'Text', 'Apply Restoration', 'Position', [20 80 150 30], ...
                'ButtonPushedFcn', @(~, ~) app.restoreImage());
            
            % Save button
            uibutton(controlPanel, 'Text', 'Save Result', 'Position', [20 30 150 30], ...
                'ButtonPushedFcn', @(~, ~) app.saveResult());
            
            % Labels for degraded and restored images
            uilabel(app.fig, 'Text', 'Degraded Image', 'Position', [300 350 120 20], 'FontSize', 12, 'FontWeight', 'bold');
            uilabel(app.fig, 'Text', 'Restored Image', 'Position', [550 350 120 20], 'FontSize', 12, 'FontWeight', 'bold');
            
            % Axes for displaying images
            app.degradedAxes = uiaxes(app.fig, 'Position', [250 70 250 250]);
            app.restoredAxes = uiaxes(app.fig, 'Position', [500 70 250 250]);
        end
        
        function loadImage(app)
            % Load degraded image
            [file, path] = uigetfile({'*.png;*.jpg;*.bmp', 'Image Files (*.png, *.jpg, *.bmp)'});
            if isequal(file, 0)
                return; % User canceled
            end
            app.degradedImage = imread(fullfile(path, file));
            imshow(app.degradedImage, 'Parent', app.degradedAxes);
            title(app.degradedAxes, 'Degraded Image');
        end
        
        function restoreImage(app)
            if isempty(app.degradedImage)
                uialert(app.fig, 'Please load a degraded image first.', 'Error');
                return;
            end
            
            % Convert to grayscale if the image is RGB
            if size(app.degradedImage, 3) == 3
                grayscaleImage = rgb2gray(app.degradedImage);
            else
                grayscaleImage = app.degradedImage;
            end
            
            % Apply median filtering for restoration
            app.restoredImage = medfilt2(grayscaleImage, [3, 3]);
            imshow(app.restoredImage, 'Parent', app.restoredAxes);
            title(app.restoredAxes, 'Restored Image');
        end
        
        function saveResult(app)
            if isempty(app.restoredImage)
                uialert(app.fig, 'No restored image to save. Please apply restoration first.', 'Error');
                return;
            end
            
            % Save restored image
            [file, path] = uiputfile({'*.png', 'PNG Image (*.png)'; '*.jpg', 'JPEG Image (*.jpg)'}, 'Save Image');
            if isequal(file, 0)
                return; % User canceled
            end
            
            imwrite(app.restoredImage, fullfile(path, file));
            uialert(app.fig, 'Restored image saved successfully.', 'Success');
        end
    end
end

