function [pos_x, pos_y, pos_z] = forward_kinematics(theta_1, theta_2, theta_3)
    % Convert angles to radians
    Th_1 = theta_1 * pi / 180;
    Th_2 = theta_2 * pi / 180;
    Th_3 = theta_3 * pi / 180;

    % Define robot arm lengths
    L_1 = 67;
    L_2 = 188;
    L_3 = 114;

    % Define the robot arm
    L(1) = Link([0 L_1 15 pi/2]);
    L(2) = Link([pi/2 0 L_2 0]);
    L(3) = Link([-pi/2 0 L_3 -pi/2]);

    Robot = SerialLink(L);
    Robot.name = 'RRR_Robot';

    % Forward kinematics
    T = Robot.fkine([Th_1 Th_2 Th_3]).T;
    pos_x = T(1, 4);
    pos_y = T(2, 4);
    pos_z = T(3, 4);
end

function [theta_1, theta_2, theta_3] = inverse_kinematics(pos_x, pos_y, pos_z)
    % Define robot arm lengths
    L_1 = 67;
    L_2 = 188;
    L_3 = 114;

    % Define the robot arm
    L(1) = Link([0 L_1 15 pi/2]);
    L(2) = Link([pi/2 0 L_2 0]);
    L(3) = Link([-pi/2 0 L_3 -pi/2]);

    Robot = SerialLink(L);
    Robot.name = 'RRR_Robot';

    % Define the transformation matrix
    T = [1 0 0 pos_x;
         0 1 0 pos_y;
         0 0 1 pos_z;
         0 0 0 1];

    % Perform inverse kinematics
    J = Robot.ikine(T, [0, 0, 0], 'mask', [1, 1, 1, 0, 0, 0]);
    theta_1 = J(1) * 180 / pi;
    theta_2 =
