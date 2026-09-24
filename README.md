/generate_manual_testcases

# CONTEXT
- System type: Web đặt khám bệnh viện 
- Module: Tối ưu trải nghiệm người dùng Luồng Booking (Phase 1)
- URL: https://beta.medpro.com.vn/chon-lich-kham?feature=booking.date&partnerId=bvgdtest&isDetail=true&behavior=
tài khoản url: username: medpro, password: fullspeed
Tài khoản đăng nhập: 0387179033/123123



- Requirement: 

#Constraint:
- Chỉ thao tác trên folder Booking
- Thao tác trên url để viết testcases
- Tất cả chỉ làm 1 lần không lặp, tối uu token hết ít nhất có thể để tạo testcase 
- Chọn dịch vụ Khám tại khoa, chọn lịch khám giờ khám bất kì linh hoạt 

npx playwright test src/tests/payment.spec.ts --headed

----------------------
