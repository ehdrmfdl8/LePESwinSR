clc;
clear all;
folder_name = 'comparison/woman/*.png';
folder = 'comparison/woman';
filelist = dir(folder_name);
N = size(filelist,1);
img_name = [];

for i = 1:N
    filename = strcat(folder,'/', filelist(i).name);
    coord_X = 120;
    coord_Y = 200;
    img = imread(filename);
    img = im2double(img);

    img = Show_enlargement(img, coord_X, coord_Y); % 240 미만 

    line_width = 3;
    img = Draw_boundingBox(img, coord_X, coord_Y, line_width);

    figure(1);
    imshow(img);

    imwrite(img,strcat('new_',filelist(i).name));

end

