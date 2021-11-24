function y = Draw_boundingBox(img, x_coord, y_coord, line_width)
    scale = 4;
    imgsize = size(img);
    width = imgsize(1);
    height = imgsize(2);
    temp = zeros(width,height,3);
    % draw object box
    for i = 1:width
        for j = 1:height
            if i > x_coord && i <= (x_coord + width/(2*scale)) && j > y_coord && j <= (y_coord + height/(2*scale))
                temp(i,j,:) = img(i,j,:);
                img(i,j,:) = 0;
                img(i,j,2) = 1;
            end
        end
    end
    for i = 1:width
        for j = 1:height
            if i > x_coord + line_width && i <= (x_coord + width/(2*scale)) - line_width && j > y_coord + line_width && j <= (y_coord + height/(2*scale)) - line_width
                img(i,j,:) = temp(i,j,:);
            end
        end
    end
    % draw enlarged box
    for i = 1:width
        for j = 1:height
            if i > width/2 && i <= width && j > height/2 && j <= height
                temp(i,j,:) = img(i,j,:);
                img(i,j,:) = 0;
                img(i,j,1) = 1;
            end
        end
    end
    for i = 1:width
        for j = 1:height
            if i > width/2 + line_width && i <= width - line_width && j > height/2 + line_width && j <= height - line_width
                img(i,j,:) = temp(i,j,:);
            end
        end
    end
    y = img;
end