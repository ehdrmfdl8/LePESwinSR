function y = Show_enlargement(img, x_coord, y_coord)
    imgsize = size(img);
    width = imgsize(1);
    height = imgsize(2);
    scale = 4;
    img2 = imresize(img, scale, 'bicubic');
    img3 = zeros(width/2,height/2,3);
    for i = 1 : width * scale
        for j = 1 : height * scale
            if i > x_coord*scale && i <= (x_coord*scale + width/2) && j > y_coord*scale && j <= (y_coord*scale + height/2)
                img3(i-x_coord*scale,j-y_coord*scale,:) = img2(i,j,:);
            end
        end
    end
    for i = 1:width
        for j = 1:height
            if i > width/2 && j > height/2
                img(i,j,:) = img3(i-width/2,j-height/2,:);
            end
        end
    end
    y = img;
end