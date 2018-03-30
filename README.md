# car
```
scrapy crawl guazi_sale -o ../data/guazi_sale.csv
```

```sql
delete from car_brand;
delete from car_car;
delete from car_model;
delete from car_tf;


-- 插入car_brand
insert into car_brand (name,first)
select brand_name,min(brand_first)
from car_sale
group by brand_name;

-- 插入car_car
insert into car_car (name,type,brand_id)
select car_name,
case
when min(car_type)='MPV' then 'mpv'
when min(car_type)='SUV' then 'suv'
when min(car_type)='皮卡' then 'pickup'
when min(car_type)='两厢轿车' then 'two'
when min(car_type)='三厢轿车' then 'three'
when min(car_type)='跑车' then 'sport'
when min(car_type)='其他' then 'other'
when min(car_type)='面包车' then 'van'
end,
min(cb.id)
from car_sale cs left join car_brand cb on cs.brand_name=cb.name
group by car_name;

--插入car_model
insert into car_model (name,car_id,price_new)
select model_name,min(cc.id),
substring(min(price_new) from (position( '价' in min(price_new))+1) for (position( '万' in min(price_new)) - position( '价' in min(price_new)) -1))
from car_sale cs left join car_car cc on cs.car_name=cc.name
where position( '价' in price_new) > 0
group by model_name;

--插入car_tf
insert into car_tf (model_id,city_id,used_months,xingshi,price_new,price)
select cm.id as model_id,
ca.id as city_id,
date_part('month', age(to_date(cs.shangpai_date,'YYYY-MM'))) as used_months,
substring(xingshi from 0 for position('万' in xingshi)) as xingshi,
cm.price_new as price_new,
substring(price from 2)
from car_sale cs left join car_model cm on cs.model_name=cm.name
left join car_area ca on cs.address=ca.city_name
where position( '价' in cs.price_new) > 0;



select count(*)
from car_model;


```