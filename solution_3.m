phoneNumber = 8264666071;
phoneStr = strrep(num2str(phoneNumber),"0","3");
coffs = zeros(1,10);

phoneArr = num2cell(char(phoneStr));
for i=1:10
    coffs(i) = str2double(phoneArr(i));
end


z = sym(-1*coffs(10));
syms x y
for i=0:3
   e = (-1)^i*(x^(3-i))*(y^i)*coffs(i+1);
   z = z + sym(e);
end

for i=0:2
   e = (-1)^i*(x^(2-i))*(y^i)*coffs(i+5);
   z = z + sym(e);
end

for i=0:1
   e = (-1)^(i+1)*(x^(1-i))*(y^i)*coffs(i+8);
   z =z+ sym(e);
end


eqn = z;
disp(eqn)
dx = diff(eqn,x);
dy = diff(eqn,y);
cp = vpasolve([dx,dy]);
fprintf("Critical Points\n");
for i=1:length(cp.x)
  cx = cp.x(i);
  cy = cp.y(i);
  fprintf("Critical Point %d: (%.6f,%.6f)\n",i,cx,cy);
end



fprintf("\n\nCritical Point Type\n");
dxx = diff(dx,x);
dxy = diff(dx,y);
dyx = diff(dy,x);
dyy = diff(dy,y);
H = [dxx dxy; dyx dyy];


for i=1:length(cp.x)
  cx = cp.x(i);
  cy = cp.y(i);
  HT = subs(H,{x,y},{cx,cy});
  fxx = HT(1,1);
  D = det(HT);
  fprintf("Critical Point %d: (%.6f,%.6f) --> ",i,cx,cy);
  if(D==0)
      fprintf("Denerated\n");
  elseif(D<0)
      fprintf("Saddle Point\n");
  elseif(D>0)
      if(fxx>0)
          fprintf("Minimum Point\n");
      elseif(fxx<0)
          fprintf("Maximum Point\n");
      end
  end
end